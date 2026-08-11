from fastapi import Header, HTTPException
from app.config import supabase

def get_current_user(authorization: str = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required")
    
    token = authorization.replace("Bearer ", "")
    
    try:
        user_response = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = user_response.user
    return user