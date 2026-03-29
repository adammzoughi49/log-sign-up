# Backend (FastAPI)

Quick instructions to install dependencies and run the API locally.

Install dependencies (from project root or inside backend folder):

```powershell
python -m pip install -r backend\requirements.txt
```

Run with uvicorn (recommended for development):

```powershell
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or run directly with Python (will call uvicorn internally, but requires uvicorn installed):

```powershell
cd backend
python main.py
```

The API will be available at http://localhost:8000

SMTP configuration (for password reset emails)
---------------------------------------------

Set these environment variables before running the server so the backend can send real emails:

- SMTP_HOST (required) — e.g. smtp.gmail.com or smtp.mailtrap.io
- SMTP_PORT (optional, default 587)
- SMTP_USER (optional)
- SMTP_PASS (optional)
- EMAIL_FROM (optional, defaults to SMTP_USER)
- SMTP_USE_TLS (optional, default true)

Example (PowerShell):

```powershell
$env:SMTP_HOST = 'smtp.example.com'
$env:SMTP_PORT = '587'
$env:SMTP_USER = 'your-smtp-username'
$env:SMTP_PASS = 'your-smtp-password'
$env:EMAIL_FROM = 'noreply@example.com'
$env:SMTP_USE_TLS = 'true'
python main.py
```

Notes:
- For development, services like Mailtrap or Ethereal are convenient because they capture emails for inspection without delivering to real inboxes.
- If using Gmail, you may need an app password and to enable access for your account.
