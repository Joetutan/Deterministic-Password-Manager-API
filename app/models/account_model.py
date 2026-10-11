from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.models.account_model import Policy

if TYPE_CHECKING:
    from app.models.vault_model import Vault


class Account(Base):
    __tablename__ = "accounts"

    id:  Mapped[int] = mapped_column(primary_key=True)

    system_name: Mapped[str] = mapped_column( String(255), nullable=False)

    user_name: Mapped[str] = mapped_column( String(255), nullable=False)

    #policy: Mapped["Policy"] = mapped_column(JSONB, nullable=False)

    last_rotated: Mapped[datetime] = mapped_column
