
from datetime import UTC, datetime

from fastapi import HTTPException, status

from app.api.auth_dependencies import get_user_meta
from app.models.account_data_model import AccountMeta
from app.models.policy_data_model import AccountPolicy
from app.models.user_model import User
from app.repository.vault_repository import VaultRepository
from app.schemas.account_schema import AccountResponse
from app.service.cryptography.account_key import gen_account_key
from app.service.cryptography.master_key import gen_master_key


class VaultService:
    def __init__(self, repository:VaultRepository) -> None:
        self.repository = repository

    def create_account(self,user:User, system_name:str, username:str,alias:str, symbols:bool, password:str ,):
        account = self.repository.get_by_alias(user.id, alias)
        if account:
            raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="An account with this alias already exists."
                )
        policy = AccountPolicy(symbols=symbols)
        meta = get_user_meta(user)
        master_key = gen_master_key(password, meta)
        if not master_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
        account_meta = AccountMeta(policy=policy, last_rotated=datetime.now(UTC), system_name=system_name, username=username)
        account= self.repository.create(user_id=user.id, alias=alias, master_key=master_key, account=account_meta)
        return AccountResponse(account_alias=account.account_alias, system_name=account.system_name,last_rotated=account_meta.last_rotated,version=account_meta.version)

    def view_accounts(self, user:User, password:str)->list[AccountResponse]:
        meta = get_user_meta(user)
        master_key = gen_master_key(password, meta)
        if not master_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
        accounts = self.repository.get_all(user_id=user.id, password=password)
        return[AccountResponse.model_validate(account) for account in accounts]
    
    def get_passkey(self, user:User, account_alias:str, password:str):
        meta = get_user_meta(user)
        master_key = gen_master_key(password, meta)
        if not master_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
        account =  self.repository.get_account(user.id, account_alias,master_key)
        return gen_account_key(master_key, account)

    def delete_account(self, user:User, account_alias:str):
        return self.repository.delete_account(user_id=user.id, account_alias=account_alias)
    
    def rotate_account(self, user:User, account_alias:str, password:str):
        ... 


