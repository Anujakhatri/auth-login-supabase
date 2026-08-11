from fastapi import Header, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import supabase

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Access token required")
    
    token = credentials.credentials
    
    try:
        user_response = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = user_response.user
    return user