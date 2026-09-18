from fastapi import APIRouter, Depends

from models import UserDB
from schemas import UserResponse
from auth import get_current_user


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: UserDB = Depends(get_current_user)
):
    return current_user