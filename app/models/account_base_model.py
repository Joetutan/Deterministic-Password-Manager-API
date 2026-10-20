import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.user_model import User


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False,index=True)

    account_alias: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    system_name: Mapped[str] = mapped_column(String(255), nullable=False)

    payload: Mapped[bytes] = mapped_column(LargeBinary,nullable=False)

    user: Mapped["User"] = relationship(back_populates="accounts")