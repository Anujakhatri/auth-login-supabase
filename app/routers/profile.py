from fastapi import APIRouter, Header, HTTPException

router = APIRouter(tags=["profile"])

@router.get("/public/info")
def public_info():
    return {"message":"Welcome straight to the public profile"}

@router.get("/protected/profile")
def protected_profile(authorization: str = Header(default=None)):
    if not authorization or not authorization.startawith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    return {"message": "Token received (not verified yet)", "token_preview": token[:10]}
