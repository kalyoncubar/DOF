# models/score_snapshot.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, DateTime, ForeignKey
from models.base import Base

class ScoreSnapshot(Base):
    __tablename__ = "score_snapshots"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    period_yyyymm: Mapped[int] = mapped_column(Integer, nullable=False)  # ör: 202601
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)

    nc_opened: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rc_opened: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    action_opened: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    action_on_time: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    action_delayed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # created_at/updated_at istersen ekleyebiliriz; MVP için zorunlu değil.

