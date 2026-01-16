# models/rc.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, DateTime, ForeignKey
from models.base import Base

class RC(Base):
    __tablename__ = "rc"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    from_comment_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("discussion_comments.id"))
    created_by: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)  # 'open' | 'closed'
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False)
