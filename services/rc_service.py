# services/rc_service.py
class RCService:
    def __init__(self, rc_repo_factory, uow, clock):
        self._rc_repo_factory = rc_repo_factory
        self._uow = uow
        self._clock = clock

    def delete_by_admin(self, rc_id: int, reason: str | None = None):
        with self._uow() as s:
            rc = self._rc_repo_factory(s)
            rc.delete(rc_id)
            return {"deleted": rc_id, "reason": reason}

    def create_from_discussion(self, comment_id: int, created_by: int):
        with self._uow() as s:
            repo = self._rc_repo_factory(s)
            new_id = repo.create(from_comment_id=comment_id, created_by=created_by, created_at=self._clock.now())
            return {"rc_id": new_id}

    def create_manual(self, created_by: int):
        with self._uow() as s:
            repo = self._rc_repo_factory(s)
            new_id = repo.create(from_comment_id=None, created_by=created_by, created_at=self._clock.now())
            return {"rc_id": new_id, "status": "open"}
