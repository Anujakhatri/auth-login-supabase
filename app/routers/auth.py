from fastapi import APIRouter, HTTPException, Depends
from app.schemas import SignupRequest, LoginRequest
from app.config import supabase
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", status_code=201)
def signup(payload: SignupRequest):
    try:
        response = supabase.auth.sign_up(
            {
                "email": payload.email,
                "password": payload.password,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return {"user": response.user}

@router.post("/login", status_code=200)
def login(payload: LoginRequest):
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": payload.email,
                "password": payload.password,
            }
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")
    
    return {
        "access_token" : response.session.access_token,
        "refresh_token" : response.session.refresh_token,
    }
    
@router.post("/logout", status_code=204)
def logout(_ = Depends(get_current_user)):
    try:
        supabase.auth.sign_out()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return None
    