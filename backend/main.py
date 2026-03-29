from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes.auth import router

import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(router, prefix="/api/auth")

@app.get("/")
def root():
    return {"message": "API is running"}


if __name__ == "__main__":
    # Allow running the app with: python main.py
    # Prefer using uvicorn in development for auto-reload: uvicorn main:app --reload
    try:
        import uvicorn
    except Exception:
        print("Missing 'uvicorn'. Install dependencies listed in requirements.txt (pip install -r requirements.txt)")
        raise

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)