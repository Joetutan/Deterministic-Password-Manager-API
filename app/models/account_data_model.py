from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from app.models.policy_data_model import AccountPolicy


@dataclass
class AccountMeta:
    policy: AccountPolicy
    last_rotated: datetime
    system_name: str
    username: str
    version: int = 1

    def to_dict(self)->dict:
        return {
            "last_rotated": self.last_rotated.isoformat(),
            "system_name": self.system_name,
            "user_name": self.username,
            "version": self.version,
            "policy": self.policy.to_dict(),

        }

    @classmethod
    def from_dict(cls, data:dict) -> AccountMeta:
        return cls(
            last_rotated=datetime.fromisoformat(data["last_rotated"]),
            system_name = data["system_name"],
            user_name = data["user_name"],
            version = data["version"],
            policy=AccountPolicy.from_dict(data["policy"])
        )


    def rotate(self, version:int)->None:
        self.version = version
        self.last_rotated = datetime.now(UTC)