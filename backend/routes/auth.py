from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from database import get_connection
from utils.helpers import hash_password, verify_password, create_token, generate_reset_token, send_email
from datetime import datetime, timedelta

router = APIRouter()

class SignupRequest(BaseModel):
    full_name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ForgotRequest(BaseModel):
    email: str

class ResetRequest(BaseModel):
    token: str
    new_password: str

@router.post("/signup")
def signup(data: SignupRequest):
    conn = get_connection()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (data.email,)).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(data.password)
    conn.execute(
        "INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)",
        (data.full_name, data.email, hashed)
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "Account created successfully"}

@router.post("/login")
def login(data: LoginRequest):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (data.email,)).fetchone()
    conn.close()
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token({"sub": str(user["id"]), "email": user["email"]})
    return {"success": True, "token": token, "full_name": user["full_name"]}

@router.post("/forgot-password")
def forgot_password(data: ForgotRequest, background: BackgroundTasks):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (data.email,)).fetchone()
    if not user:
        # Don't reveal whether the email exists
        return {"success": True, "message": "If this email exists, a reset link was sent"}
    token = generate_reset_token()
    expires = (datetime.utcnow() + timedelta(minutes=15)).isoformat()
    conn.execute(
        "UPDATE users SET reset_token = ?, reset_token_expires = ? WHERE email = ?",
        (token, expires, data.email)
    )
    conn.commit()
    conn.close()

    reset_url = f"http://localhost:5173/reset-password?token={token}"
    subject = "Password reset for your account"
    body = (
        f"You requested a password reset. Click or paste the link below to reset your password (valid for 15 minutes):\n\n"
        f"{reset_url}\n\nIf you didn't request this, ignore this email."
    )
    html = (
        f"<p>You requested a password reset. Click the link below to reset your password (valid for 15 minutes):</p>"
        f"<p><a href=\"{reset_url}\">Reset password</a></p>"
    )

    # Schedule sending the email in the background so the endpoint returns fast.
    try:
        background.add_task(send_email, data.email, subject, body, html)
    except Exception as e:
        # If scheduling fails for any reason, attempt a best-effort synchronous send and print the link.
        print(f"Failed to schedule background email: {e}")
        sent = send_email(data.email, subject, body, html)
        if not sent:
            print(f"\n=== RESET LINK ===\n{reset_url}\n==================\n")

    return {"success": True, "message": "Reset link sent — check your email or terminal for now"}

@router.post("/reset-password")
def reset_password(data: ResetRequest):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE reset_token = ?", (data.token,)).fetchone()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    if datetime.utcnow() > datetime.fromisoformat(user["reset_token_expires"]):
        raise HTTPException(status_code=400, detail="Token has expired")
    hashed = hash_password(data.new_password)
    conn.execute(
        "UPDATE users SET password_hash = ?, reset_token = NULL, reset_token_expires = NULL WHERE id = ?",
        (hashed, user["id"])
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "Password updated successfully"}