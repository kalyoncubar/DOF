# services/discussion_service.py
from repositories.discussion_repository import DiscussionRepository
from repositories.settings_repository import SettingsRepository

class DiscussionService:
    def __init__(self, disc_repo_factory, rc_service, settings_repo_factory, uow, clock=None):
        self._disc_repo_factory = disc_repo_factory
        self._rc_service = rc_service
        self._settings_repo_factory = settings_repo_factory
        self._uow = uow
        self._clock = clock

    def add_comment(self, nc_id: int, user_id: int, text: str, parent_id=None):
        with self._uow() as s:
            disc = self._disc_repo_factory(s)
            return disc.add_comment(nc_id, user_id, text, parent_id)

    def vote(self, comment_id: int, user_id: int, delta: int):
        with self._uow() as s:
            disc = self._disc_repo_factory(s)
            settings = self._settings_repo_factory(s)
            score = disc.add_vote(comment_id, user_id, delta)
            threshold = settings.get_int("discussion_threshold", 5)

        # Eşik aşıldıysa RC oluştur (geri alma yok)
        if score >= threshold:
            # Not: RC'yi kimin adına açacağımız ürüne göre değişir.
            # Basit kural: threshold'u tetikleyen en son oy veren kullanıcıyı "created_by" kabul ediyoruz.
            self._rc_service.create_from_discussion(comment_id=comment_id, created_by=user_id)

        return {"score": score, "threshold": threshold}
