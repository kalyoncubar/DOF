# services/nc_service.py
class NCService:
    """
    MVP: NC open/close/reopen.
    - NC kapanması MVP kapsamı dışında demiştik; burada sadece open/closed state'lerini yönetiyoruz.
    """
    def __init__(self, nc_repo_factory, uow, clock):
        """
        nc_repo_factory(session) -> NCRepository
        uow: UnitOfWork
        clock: utils.clock.Clock
        """
        self._nc_repo_factory = nc_repo_factory
        self._uow = uow
        self._clock = clock

    def open(self, title: str, opened_by: int) -> dict:
        if not title or not title.strip():
            raise ValueError("Başlık zorunlu")
        with self._uow() as s:
            repo = self._nc_repo_factory(s)
            new_id = repo.create(title=title.strip(), opened_by=opened_by, created_at=self._clock.now())
            return {"id": new_id, "status": "open", "title": title.strip(), "opened_by": opened_by}

    def list_all(self) -> list[dict]:
        with self._uow() as s:
            repo = self._nc_repo_factory(s)
            return repo.list_all()

    def get(self, nc_id: int) -> dict:
        with self._uow() as s:
            repo = self._nc_repo_factory(s)
            nc = repo.get_by_id(nc_id)
            if not nc:
                raise ValueError("NC bulunamadı")
            return nc

    def update_title(self, nc_id: int, title: str) -> dict:
        if not title or not title.strip():
            raise ValueError("Başlık zorunlu")
        with self._uow() as s:
            repo = self._nc_repo_factory(s)
            nc = repo.get_by_id(nc_id)
            if not nc:
                raise ValueError("NC bulunamadı")
            repo.update_title(nc_id, title.strip())
            nc["title"] = title.strip()
            return nc

    def close(self, nc_id: int, admin_user_id: int) -> dict:
        with self._uow() as s:
            repo = self._nc_repo_factory(s)
            nc = repo.get_by_id(nc_id)
            if not nc:
                raise ValueError("NC bulunamadı")
            if str(nc.get("status")) == "closed":
                raise ValueError("NC zaten kapalı")
            repo.set_state(nc_id, new_state="closed", closed_by_admin_id=admin_user_id)
            return {"id": nc_id, "status": "closed", "closed_by": admin_user_id}

    def reopen(self, nc_id: int, admin_user_id: int) -> dict:
        with self._uow() as s:
            repo = self._nc_repo_factory(s)
            nc = repo.get_by_id(nc_id)
            if not nc:
                raise ValueError("NC bulunamadı")
            if str(nc.get("status")) == "open":
                raise ValueError("NC zaten açık")
            repo.set_state(nc_id, new_state="open", reopened_by_admin_id=admin_user_id)
            return {"id": nc_id, "status": "open", "reopened_by": admin_user_id}
