import json

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account_base_model import Account
from app.models.account_data_model import AccountMeta
from app.service.cryptography.account_crypt import AccountCrypt


class VaultRepository:
    def __init__(self, db:Session) -> None:
        self.db = db
        self.crypt = AccountCrypt()

    def create(self, user_id:int,alias:str, master_key:bytes, account: AccountMeta):
        
        data = json.dumps(account.to_dict(),indent=4).encode("utf-8")
        encrypted = self.crypt.encrypt_account(data, master_key)
        account = Account(user_id=user_id, account_alias=alias ,system_name=account.system_name, payload=encrypted)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def get_account(self, user_id:int, account_alias:str, master_key:bytes)-> AccountMeta:

        statement = select(Account).where(Account.user_id==user_id).where(Account.account_alias==account_alias)
        account = self.db.scalar(statement)

        encrypted = account.payload
        data = self.crypt.decrypt_account(master_key, encrypted)
        payload = json.loads(data.decode("utf-8"))

        return AccountMeta.from_dict(payload)

    def get_by_alias(self, user_id:int, alias:str)-> Account | None:
        statement = select(Account).where(Account.user_id==user_id).where(Account.account_alias==alias)
        account = self.db.scalar(statement)
        return account

    def delete_account(self,user_id:int,account_alias:str) -> None:
        statement = select(Account).where(Account.user_id==user_id).where(Account.account_alias==account_alias)
        account = self.db.scalar(statement)
        self.db.delete(account)
        self.db.commit()

    def get_all(self, user_id:int)->list[AccountMeta]:

        statement = select(Account).where(Account.user_id==user_id)
        payload = self.db.scalars(statement).all()
        #accounts = []
        #for account in payload:
        #    accounts.append(AccountMeta.fromdict(account))
        return payload