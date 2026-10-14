
from typing import Annotated

from fastapi import APIRouter, Depends, Form, status

#from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.auth_dependencies import get_current_user
from app.config.database import get_db
from app.models.user_model import User
from app.repository.vault_repository import VaultRepository
from app.schemas.account_schema import AccountCreate, AccountResponse
from app.service.vault_service import VaultService

router = APIRouter(prefix="/api/v1/vault", tags=["vault"])

def get_vault_service(db: Annotated[Session, Depends(get_db)])->VaultService:
    return VaultService(VaultRepository(db))


@router.post("",response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def add_account(
    symbols: Annotated[bool, Form()],
    master_password: Annotated[str, Form()],
    username: Annotated[str, Form()],
    system_name: Annotated[str, Form()],
    current_user: Annotated[User , Depends(get_current_user)], 
    service: Annotated[VaultService, Depends(get_vault_service)] ) -> AccountResponse:
    account = service.create_account(user=current_user,system_name=system_name,username=username,symbols=symbols, password=master_password)

    return AccountResponse(system_name=account.system_name )

@router.get("")
def get_passkey(
    current_user: Annotated[User , Depends(get_current_user)], 
    data: AccountCreate,
    service: Annotated[VaultService, Depends(get_vault_service)],
    master_password: Annotated[str, Form()]):

    return service.get_account(user=current_user, system_name=data.system_name, password=master_password)

