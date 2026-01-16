# models/discussion_vote.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, ForeignKey, UniqueConstraint
from models.base import Base

class DiscussionVote(Base):
    __tablename__ = "discussion_votes"
    comment_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("discussion_comments.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), primary_key=True)
    delta: Mapped[int] = mapped_column(Integer)  # -1 | 1
    __table_args__ = (UniqueConstraint("comment_id","user_id", name="uq_vote"),)
