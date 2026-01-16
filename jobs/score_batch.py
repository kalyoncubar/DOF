# jobs/score_batch.py
from datetime import datetime
from services.uow import UnitOfWork
from config.db import SessionFactory
from repositories.score_repository import ScoreRepository
from repositories.settings_repository import SettingsRepository
from services.score_service import ScoreService

def score_repo_factory(s): return ScoreRepository(s)
def settings_repo_factory(s): return SettingsRepository(s)

def run(yyyymm: int | None = None):
    if yyyymm is None:
        now = datetime.utcnow()
        yyyymm = now.year*100 + now.month
    uow = UnitOfWork(SessionFactory)
    svc = ScoreService(score_repo_factory, settings_repo_factory, uow)
    svc.monthly_snapshot(yyyymm)
    print({"snapshot_done_for": yyyymm})

if __name__ == "__main__":
    run()
