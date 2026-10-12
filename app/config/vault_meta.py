from __future__ import annotations

import base64
import secrets
from dataclasses import dataclass

from app.config.env_settings import settings


@dataclass
class VaultMeta:
    salt: str =  base64.b64encode(secrets.token_bytes(16)).decode("ascii")
    algorithm: str = settings.algorithm
    cipher: str = settings.cipher
    hash_length: int = settings.hash_length
    time_cost: int = settings.time_cost
    memory_cost: int = settings.memory_cost
    parallelism: int = settings.parallelism
    version: int = 1

    def to_dict(self) -> dict:
        return {
            "salt": self.salt,
            "algorithm": self.algorithm,
            "cipher": self.cipher,
            "hash_length": self.hash_length,
            "time_cost": self.time_cost,
            "memory_cost": self.memory_cost,
            "parallelism": self.parallelism,
            "version": self.version,
        }

    @classmethod
    def dict_to_meta( cls, data:dict) -> VaultMeta:
        return cls(
            salt = data["salt"],
            algorithm = data["algorithm"],
            cipher = data["cipher"],
            hash_length = data["hash_length"],
            time_cost = data["time_cost"],
            memory_cost = data["memory_cost"],
            parallelism = data["parallelism"],
            version=data["version"]
        )