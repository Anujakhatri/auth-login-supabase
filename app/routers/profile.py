from fastapi import APIRouter

from app.dependencies import CurrentUser
from app.routers.auth import to_user_response
from app.schemas import DashboardResponse, MessageResponse, ProfileResponse

router = APIRouter(tags=["Examples"])


@router.get("/public/info", response_model=MessageResponse)
def public_info() -> MessageResponse:
    return MessageResponse(message="This endpoint is publicly accessible.")


@router.get("/protected/profile", response_model=ProfileResponse)
def profile(current_user: CurrentUser) -> ProfileResponse:
    return ProfileResponse(
        user=to_user_response(current_user),
        message="Authenticated profile loaded successfully.",
    )


@router.get("/protected/dashboard", response_model=DashboardResponse)
def dashboard(current_user: CurrentUser) -> DashboardResponse:
    return DashboardResponse(
        user_id=str(current_user.id),
        message="Authenticated dashboard loaded successfully.",
        data={"account_type": "supabase_user"},
    )
