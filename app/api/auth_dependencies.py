import json
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config.auth_security import security
from app.config.database import get_db
from app.models.meta_data_model import AccountMeta
from app.models.user_model import User
from app.repository.user_repository import UserRepository
from app.service.cryptography.meta_crypt import MetaCrypt

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_user_repository(db: Annotated[Session , Depends(get_db)])->UserRepository:
    return UserRepository(db)

def get_current_user(token: Annotated[str,Depends(oauth2_schema)], db: Annotated[Session, Depends(get_db)])-> User:

        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})

        try:
            user_id = security.verify_access_token(token)

            if user_id is None:
                raise credentials_exception
            
            user_id = int(user_id)

        except (ValueError, TypeError) as exc:
            raise credentials_exception from exc
        
        repository = UserRepository(db)

        user = repository.get_by_id(user_id)

        if user is None:
            raise credentials_exception

        return user

def gen_user_meta():
        meta = AccountMeta()
        data = json.dumps(meta.to_dict(),indent=4).encode("utf-8")
        #encrypted = MetaCrypt.encrypt_meta(data, master_key)
        return data

def get_user_meta(user:User):
        data = user.meta
        #data =MetaCrypt.decrypt_meta(master_key=master_key, encrypted=encrypted)
        payload = json.loads(data.decode("utf-8"))
        meta = AccountMeta()
        return meta.from_dict(payload=payload)
