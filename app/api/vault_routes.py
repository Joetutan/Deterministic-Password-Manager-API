'''
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.auth_dependencies import get_current_user
from app.config.database import get_db
from app.models.user_model import User
from app.repository.vault_repository import VaultRepository
from app.schemas.policy_schema import AccountPolicy
from app.service.vault_service import VaultService

router = APIRouter(prefix="/api/v1/vault", tags=["vault"])

def get_vault_service(db: Annotated[Session, Depends(get_db)])->VaultService:
    return VaultService(VaultRepository(db))

@router.post("")
def add_account(
    current_user: Annotated[User, Depends(get_current_user)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    system_name: str, 
    policy:AccountPolicy,
    service: Annotated[VaultService, Depends(get_vault_service)]):
    return service.create_account(user=current_user, system_name=system_name, policy=policy, password=form_data.password)
'''