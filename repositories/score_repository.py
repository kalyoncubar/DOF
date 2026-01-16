# repositories/score_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from models.score_snapshot import ScoreSnapshot

class ScoreRepository:
    def __init__(self, s: Session): self.s = s

    def upsert_snapshot(self, snap: ScoreSnapshot):
        # basit upsert: aynı period_yyyymm + user_id varsa update, yoksa insert
        existing = (
            self.s.query(ScoreSnapshot)
            .filter(ScoreSnapshot.period_yyyymm == snap.period_yyyymm,
                    ScoreSnapshot.user_id == snap.user_id)
            .first()
        )
        if existing:
            for f in ("nc_opened","rc_opened","action_opened","action_on_time","action_delayed","score"):
                setattr(existing, f, getattr(snap, f))
        else:
            self.s.add(snap)
