from __future__ import annotations

import base64
import secrets
from dataclasses import dataclass

from app.config.env_settings import settings


@dataclass(slots=True, frozen=True)
class AccountMeta:
                salt: bytes = secrets.token_bytes(16)
                algorithm: str = settings.algorithm
                cipher : str = settings.cipher
                hash_length: int  = settings.hash_length
                time_cost : int = settings.time_cost
                memory_cost: int = settings.memory_cost
                parallelism: int = settings.parallelism
                version:int = 1

                def to_dict(self) -> dict:
                        return {
                                "version": self.version,
                                "algorithm": self.algorithm,
                                "salt": base64.b64encode(self.salt).decode("ascii"),
                                "time_cost": self.time_cost,
                                "memory_cost": self.memory_cost,
                                "hash_length": self.hash_length,
                                "parallelism": self.parallelism,
                                "cipher": self.cipher
                        }

                @classmethod
                def from_dict(cls, payload:dict) -> AccountMeta:
                        return cls(
                                salt=base64.b64decode(payload["salt"]),
                                algorithm = payload["algorithm"],
                                cipher=payload["cipher"],
                                hash_length=payload["hash_length"],
                                time_cost=payload["time_cost"],
                                memory_cost=payload["memory_cost"],
                                parallelism=payload["parallelism"],
                                version=payload["version"]
                        )
