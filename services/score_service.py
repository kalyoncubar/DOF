# services/score_service.py
from models.score_snapshot import ScoreSnapshot

class ScoreService:
    def __init__(self, score_repo_factory, settings_repo_factory, uow):
        self._score_repo_factory = score_repo_factory
        self._settings_repo_factory = settings_repo_factory
        self._uow = uow

    def monthly_snapshot(self, yyyymm: int):
        # Not: Aşağıdaki sayımlar MVP için pseudo; gerçek sayımlar prod sorgularıyla doldurulacak.
        with self._uow() as s:
            score_repo = self._score_repo_factory(s)
            settings = self._settings_repo_factory(s)

            # katsayıları ayarla (settings)
            K = {
                "nc": int(settings.get_int("score_nc_open", 2)),
                "rc": int(settings.get_int("score_rc_open", 3)),
                "ac": int(settings.get_int("score_action_create", 1)),
                "ont": int(settings.get_int("score_action_on_time", 5)),
                "del": int(settings.get_int("score_action_delay", -3)),
            }

            # TODO: burada gerçek sayımlar yapılacak (repositories ile)
            # örnek dummy tek kullanıcı 1 için:
            data = {
                1: dict(nc=0, rc=0, ac=0, ont=0, dly=0),
            }

            for user_id, v in data.items():
                total = v["nc"]*K["nc"] + v["rc"]*K["rc"] + v["ac"]*K["ac"] + v["ont"]*K["ont"] + v["dly"]*K["del"]
                snap = ScoreSnapshot(
                    period_yyyymm=yyyymm,
                    user_id=user_id,
                    nc_opened=v["nc"],
                    rc_opened=v["rc"],
                    action_opened=v["ac"],
                    action_on_time=v["ont"],
                    action_delayed=v["dly"],
                    score=total,
                )
                score_repo.upsert_snapshot(snap)
