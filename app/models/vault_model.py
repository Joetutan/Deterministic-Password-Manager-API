from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.models.account_model import Account

if TYPE_CHECKING:
    from app.models.user_model import User


class Vault(Base):
    __tablename__ = "vaults"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    encrypted_data: Mapped[bytes] = mapped_column(LargeBinary,nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    #accounts: Mapped[dict["Account"]] = relationship(back_populates="vault", cascage="all, delete-orphan")
    accounts: Mapped[list["Account"]] = relationship(back_populates="vault",cascade="all, delete-orphan")

    user: Mapped["User"] = relationship(back_populates="vault")

    #created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc),nullable=False)
    #updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc),onupdate=lambda: datetime.now(timezone.utc),nullable=False)

