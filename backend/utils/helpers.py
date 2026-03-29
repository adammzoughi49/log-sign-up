from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import secrets
import os
import smtplib
from email.message import EmailMessage
import ssl

SECRET_KEY = "8461532"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)


def send_email(to_email: str, subject: str, body: str, html: str | None = None) -> bool:
    """Send an email using SMTP settings from environment variables.

    Environment variables used:
      - SMTP_HOST (required)
      - SMTP_PORT (defaults to 587)
      - SMTP_USER (optional)
      - SMTP_PASS (optional)
      - EMAIL_FROM (defaults to SMTP_USER)
      - SMTP_USE_TLS ("true"/"false", defaults to true)

    Returns True on success, False on failure.
    """
    host = os.environ.get("SMTP_HOST")
    if not host:
        print("SMTP_HOST not configured; cannot send email")
        return False

    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASS")
    from_addr = os.environ.get("EMAIL_FROM") or user or f"noreply@{host}"
    use_tls = os.environ.get("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes")

    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)
    if html:
        msg.add_alternative(html, subtype="html")

    import time
    import traceback

    # Try a couple of times in case of transient network errors
    attempts = 2
    for attempt in range(1, attempts + 1):
        try:
            # Prefer STARTTLS when use_tls is true (common on port 587)
            if use_tls:
                context = ssl.create_default_context()
                with smtplib.SMTP(host, port, timeout=10) as server:
                    server.ehlo()
                    try:
                        server.starttls(context=context)
                        server.ehlo()
                    except Exception:
                        # If STARTTLS fails (some servers/ports), try SSL fallback below
                        raise
                    if user and password:
                        server.login(user, password)
                    server.send_message(msg)
            else:
                # SSL (direct TLS) connection on port 465 or when use_tls is false
                with smtplib.SMTP_SSL(host, port, timeout=10) as server:
                    if user and password:
                        server.login(user, password)
                    server.send_message(msg)

            return True

        except Exception as e:
            # If STARTTLS failed and we haven't tried SSL yet, attempt SMTP_SSL as a fallback
            tb = traceback.format_exc()
            print(f"Attempt {attempt} failed to send email to {to_email}: {e}\n{tb}")

            # If we used STARTTLS and it failed, try direct SSL once (on typical SSL port 465)
            if use_tls and attempt == 1:
                ssl_port = int(os.environ.get("SMTP_SSL_PORT", "465"))
                try:
                    with smtplib.SMTP_SSL(host, ssl_port, timeout=10) as server:
                        if user and password:
                            server.login(user, password)
                        server.send_message(msg)
                    return True
                except Exception as e2:
                    tb2 = traceback.format_exc()
                    print(
                        f"Fallback SMTP_SSL also failed for {to_email} on port {ssl_port}: {e2}\n{tb2}\n"
                        f"This often means the host/port combination is incorrect, an HTTP proxy is intercepting the connection, or the SMTP provider requires different auth (e.g. app password)."
                    )

            # Wait a bit before retrying
            if attempt < attempts:
                time.sleep(1)

    return False
