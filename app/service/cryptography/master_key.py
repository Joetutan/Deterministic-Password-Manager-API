

from app.models.meta_data_model import AccountMeta
from argon2.low_level import Type, hash_secret_raw


def gen_master_key( master_password: str, meta:AccountMeta) -> bytes:
    return hash_secret_raw(
                secret=master_password.encode("utf-8"),
                salt=meta.salt,
                time_cost=meta.time_cost,
                memory_cost=meta.memory_cost,
                parallelism=meta.parallelism,
                hash_len=meta.hash_length,
                type=Type.ID
                )