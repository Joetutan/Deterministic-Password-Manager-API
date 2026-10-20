
from typing import Annotated

from fastapi import APIRouter, Depends, Form, status

#from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.auth_dependencies import get_current_user
from app.config.database import get_db
from app.models.user_model import User
from app.repository.vault_repository import VaultRepository
from app.schemas.account_schema import AccountResponse
from app.schemas.pass_schema import PassResponse
from app.service.vault_service import VaultService

router = APIRouter(prefix="/api/v1/vault", tags=["vault"])

def get_vault_service(db: Annotated[Session, Depends(get_db)])->VaultService:
    return VaultService(VaultRepository(db))


@router.post("",response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def add_account(
    symbols: Annotated[bool, Form()],
    master_password: Annotated[str, Form()],
    account_alias:Annotated[str, Form()],
    username: Annotated[str, Form()],
    system_name: Annotated[str, Form()],
    current_user: Annotated[User , Depends(get_current_user)], 
    service: Annotated[VaultService, Depends(get_vault_service)] ) -> AccountResponse:
    return service.create_account(user=current_user,system_name=system_name,username=username,alias=account_alias, symbols=symbols, password=master_password)


@router.post("/{system_name}/generate", response_model=PassResponse)
def get_passkey(
    current_user: Annotated[User, Depends(get_current_user)],
    account_alias: Annotated[str, Form()],
    service: Annotated[VaultService, Depends(get_vault_service)],
    master_password: Annotated[str, Form()],
):
    passkey = service.get_account(user=current_user,account_alias=account_alias,password=master_password)
    return PassResponse(password=passkey)

@router.patch("/{account_id}", response_model=AccountResponse,status_code=status.HTTP_201_CREATED)
def rotate():
    ...

@router.get("", response_model=list[AccountResponse])
def view_accounts(service:Annotated[VaultService, Depends(get_vault_service)], current_user:Annotated[User, Depends(get_current_user)], master_password:Annotated[str,Form])->list[AccountResponse]:
    return service.view_accunts(user=current_user, password=master_password)

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account():
    ...
