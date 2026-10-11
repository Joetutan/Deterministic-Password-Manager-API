from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config.env_settings import settings
from app.config.vault_meta import VaultMeta
from app.models.user_model import User


class UserRepository:
    def __init__(self, db:Session)->None:
        self.db = db

    def create(self, username:str, email:str, password_hash:str) -> User:
        vault_meta = VaultMeta.create(
            algorithm=settings.algorithm,
            cipher=settings.cipher,
            hash_length=settings.hash_length,
            time_cost=settings.time_cost,
            memory_cost=settings.memory_cost,
            parallelism=settings.parallelism
        )
        user = User(username=username, email=email, password_hash=password_hash, vault_meta=vault_meta)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id:int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

    def get_by_email(self, email:str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def get_by_username(self, username:str) -> User | None:
            statement = select(User).where(User.username == username)
            return self.db.scalar(statement)
