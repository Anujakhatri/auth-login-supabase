from fastapi import APIRouter, Depends
from app.dependencies import get_current_user

router = APIRouter(tags=["profile"])

@router.get("/public/info")
def public_info():
    return {"message":"Welcome straight to the public profile"}

@router.get("/protected/profile")
def protected_profile(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at,
    }

@router.get("/protected/dashboard")
def protected_dashboard(current_user = Depends(get_current_user)):
    return {
        "message": f"Welcome to the dashboard, {current_user.email}!",
    }