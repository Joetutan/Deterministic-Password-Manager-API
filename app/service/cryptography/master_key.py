from app.config.vault_meta import VaultMeta
from argon2.low_level import Type, hash_secret_raw


class MasterKDF:

    def generate_key(self, master_password: str, meta: VaultMeta) -> bytes:
        return hash_secret_raw(secret=master_password,
                               salt=meta.salt,
                               time_cost= meta.time_cost,
                               memory_cost=meta.memory_cost,
                               parallelism=meta.parallelism,
                               hash_len=meta.hash_length,
                               type=Type.ID
                               )