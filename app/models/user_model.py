from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, LargeBinary, String, func
from sqlalchemy.orm import Mapped, composite, mapped_column

from app.config.database import Base
from app.config.vault_meta import VaultMeta


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[int] = mapped_column(String(255), unique=True, nullable=False)

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    vault_meta: Mapped[VaultMeta] = composite(
        VaultMeta,
        mapped_column("vault_salt", LargeBinary(16), nullable=False),
        mapped_column("vault_algorithm", String(32), nullable=False),
        mapped_column("vault_cipher", String(32), nullable=False),
        mapped_column("vault_hash_length", Integer, nullable=False),
        mapped_column("vault_time_cost", Integer, nullable=False),
        mapped_column("vault_memory_cost", Integer, nullable=False),
        mapped_column("vault_parallelism", Integer, nullable=False),
        mapped_column("vault_version", Integer, nullable=False, default=1)
    )


