import base64

from pydantic import BaseModel, field_validator


class VaultMetaResponse(BaseModel):
    salt: str
    nonce: str
    algorithm: str
    cipher: str
    hash_length: int
    time_cost: int
    memory_cost: int
    parallelism: int
    version: int = 1

    @field_validator("salt", "nonce", mode="before")
    @classmethod
    def encode_binary(cls, value: bytes | str) -> str:
        if isinstance(value, bytes):
            return base64.b64encode(value).decode("ascii")
        return value