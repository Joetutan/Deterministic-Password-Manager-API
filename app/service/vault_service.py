
from datetime import UTC, datetime

from fastapi import HTTPException, status

from app.api.auth_dependencies import get_user_meta
from app.models.account_data_model import AccountMeta
from app.models.policy_data_model import AccountPolicy
from app.models.user_model import User
from app.repository.vault_repository import VaultRepository
from app.service.cryptography.account_key import gen_account_key
from app.service.cryptography.master_key import gen_master_key


class VaultService:
    def __init__(self, repository:VaultRepository) -> None:
        self.repository = repository

    def create_account(self,user:User, system_name:str, username:str, symbols:bool, password:str ):

        account = self.repository.get_by_system_name(user.id, system_name)

        if account:
            raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="An account with this system name already exists.",
                )

        policy = AccountPolicy(symbols=symbols)
        
        meta = get_user_meta(user)

        master_key = gen_master_key(password, meta)

        if not master_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")

        account_meta = AccountMeta(policy=policy, last_rotated=datetime.now(UTC), system_name=system_name, username=username)
        
        return self.repository.create(user.id, master_key, account_meta)

    def get_account(self, user:User, system_name:str, password:str):
        
        meta = get_user_meta(user)

        master_key = gen_master_key(password, meta)

        if not master_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")

        account =  self.repository.get_account(user.id,system_name,master_key)

        return gen_account_key(master_key, account)

