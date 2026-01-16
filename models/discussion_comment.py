# models/discussion_comment.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, DateTime, ForeignKey
from models.base import Base

class DiscussionComment(Base):
    __tablename__ = "discussion_comments"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nc_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("nc.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("discussion_comments.id"))
    text: Mapped[str] = mapped_column(String)  # NVARCHAR(MAX) eşleniği migration ile ayarlanabilir
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False)
    votes = relationship("DiscussionVote", backref="comment")
