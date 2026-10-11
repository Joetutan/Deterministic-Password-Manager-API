import secrets
from dataclasses import dataclass


@dataclass
class VaultMeta:
    salt: bytes
    algorithm: str
    cipher: str
    hash_length: int
    time_cost: int
    memory_cost: int
    parallelism: int
    version: int = 1

    @classmethod
    def create(cls, *, algorithm:str, cipher:str, hash_length:int,time_cost:int, memory_cost:int, parallelism:int) -> "VaultMeta":
        return cls(
            salt=secrets.token_bytes(16),
            algorithm=algorithm,
            cipher=cipher,
            hash_length= hash_length,
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism
        )