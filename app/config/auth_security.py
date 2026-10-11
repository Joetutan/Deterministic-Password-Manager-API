from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config.env_settings import settings

password_hash = PasswordHash.recommended()

class SecurityControl:
    
    def hash_password(self, password: str)-> str:
        return password_hash.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return password_hash.verify(password, hashed_password)

    def create_access_token(self, user_id: int) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        payload = {"sub": str(user_id),"exp": expires_at}
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    def verify_access_token(self, token: str):
        payload = jwt.decode(token, settings.jwt_secret, algorithms=settings.jwt_algorithm)
        return payload.get("sub")

security = SecurityControl()