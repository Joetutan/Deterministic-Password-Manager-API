from app.models.account_model import Account
from app.models.user_model import User
from app.repository.vault_repository import VaultRepository
from app.schemas.policy_schema import AccountPolicy
from app.service.cryptography import get_payload
from app.service.cryptography.master_key import MasterKDF


class VaultService:
    def __init__(self, repository:VaultRepository) -> None:
        self.repository = repository

    def create_account(user:User, system_name: str, policy:AccountPolicy, password:str):

        
        ...