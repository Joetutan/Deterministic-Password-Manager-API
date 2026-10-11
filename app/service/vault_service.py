from app.repository.vault_repository import VaultRepository


class VaultService:
    def __init__(self, repository:VaultRepository) -> None:
        self.repository = repository

    def initialize(user_id:int, master_pass:str):
        ...