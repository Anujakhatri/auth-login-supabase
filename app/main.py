from fastapi import FastAPI
from app.routers import auth, profile

app = FastAPI(
    title = "Flyrank Auth API",
    description ="Secure API with Supabase Auth — signup, login, logout, and protected routes.",
    version = "1.0.0"
)

app.include_router(auth.router)

@app.get("/")
def health_check():
    return {"status": "Server running and connected to Supabase"}
