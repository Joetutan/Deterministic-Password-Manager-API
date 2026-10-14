from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth_dependencies import get_current_user, get_user_repository
from app.repository.user_repository import UserRepository
from app.schemas.auth_schema import ResponseToken, UserCreate, UserResponse
from app.service.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

def get_auth_service(repository: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthService:
    return AuthService(repository)

@router.post("/register",response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, service: Annotated[AuthService, Depends(get_auth_service)])->UserResponse:
    return service.register(username=data.username, email=data.email, password=data.password)

@router.post("/login", response_model=ResponseToken)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: Annotated[AuthService, Depends(get_auth_service)]) -> ResponseToken:
    access_token = service.login(email=form_data.username, password=form_data.password)
    return ResponseToken(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
def get_me(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return current_user