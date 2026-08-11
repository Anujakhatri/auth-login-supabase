from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from supabase import Client

from app.config import get_supabase
from app.dependencies import CurrentUser
from app.schemas import AuthResponse, Credentials, MessageResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
Supabase = Annotated[Client, Depends(get_supabase)]


def to_user_response(user: Any) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        email=user.email,
        role=getattr(user, "role", None),
        confirmed_at=getattr(user, "confirmed_at", None),
    )


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(credentials: Credentials, supabase: Supabase) -> AuthResponse:
    try:
        result = supabase.auth.sign_up(
            {"email": credentials.email, "password": credentials.password}
        )
        session = result.session
        return AuthResponse(
            user=to_user_response(result.user) if result.user else None,
            access_token=session.access_token if session else None,
            refresh_token=session.refresh_token if session else None,
            expires_in=session.expires_in if session else None,
        )
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=AuthResponse)
def login(credentials: Credentials, supabase: Supabase) -> AuthResponse:
    try:
        result = supabase.auth.sign_in_with_password(
            {"email": credentials.email, "password": credentials.password}
        )
        session = result.session
        return AuthResponse(
            user=to_user_response(result.user) if result.user else None,
            access_token=session.access_token if session else None,
            refresh_token=session.refresh_token if session else None,
            expires_in=session.expires_in if session else None,
        )
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials") from exc


@router.post("/logout", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: CurrentUser, supabase: Supabase) -> Response:
    try:
        supabase.auth.sign_out()
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unable to end the session") from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
