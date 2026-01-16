# models/action_history.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, DateTime, ForeignKey
from models.base import Base  # Projende Base nerede ise oradan import et

class ActionHistory(Base):
    __tablename__ = "action_history"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    action_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("actions.id"), nullable=False)
    old_state: Mapped[str | None] = mapped_column(String(16), nullable=True)
    new_state: Mapped[str] = mapped_column(String(16), nullable=False)
    changed_by: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    changed_at: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False)
    note: Mapped[str | None] = mapped_column(String(500), nullable=True)
