# models/action.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, DateTime, ForeignKey
from models.base import Base

class Action(Base):
    __tablename__ = "actions"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    rc_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("rc.id"), nullable=False)
    assignee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    state: Mapped[str] = mapped_column(String(16), nullable=False)  # CHECK constraint migration'da
    due_date: Mapped[DateTime | None] = mapped_column(DateTime(timezone=False))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False)
    closed_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=False))
    history = relationship("ActionHistory", backref="action")
