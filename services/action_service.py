# services/action_service.py
from __future__ import annotations
from typing import Optional
from datetime import datetime

class ActionService:
    """
    İş kuralları:
    - create -> state = 'oneri'
    - plan   : oneri -> planli
    - complete: planli -> tamamlanmis
    - close(approved=True)  : tamamlanmis -> kapali_onay
    - close(approved=False) : tamamlanmis -> kapali_red  (+ otomatik V2)
    Transaction sınırı service katmanındadır.
    """

    def __init__(self, action_repo_factory, rc_repo_factory, user_repo_factory, clock, uow):
        """
        action_repo_factory(session) -> ActionRepository
        rc_repo_factory(session) -> RCRepository
        user_repo_factory(session) -> UserRepository
        clock: utils.clock.Clock  (now())
        uow: services.uow.UnitOfWork (callable context manager)
        """
        self._action_repo_factory = action_repo_factory
        self._rc_repo_factory = rc_repo_factory
        self._user_repo_factory = user_repo_factory
        self._clock = clock
        self._uow = uow

    # ---- Transitions ----

    def propose(self, rc_id: int, assignee_id: int, due_date: Optional[datetime] = None) -> int:
        """Yeni action açar; başlangıç state 'oneri'."""
        with self._uow() as s:
            actions = self._action_repo_factory(s)
            rcs = self._rc_repo_factory(s)
            users = self._user_repo_factory(s)

            assert rcs.exists(rc_id), "RC not found"
            assert users.exists_active(assignee_id), "Assignee inactive"

            new_id = actions.insert(
                rc_id=rc_id,
                assignee_id=assignee_id,
                state="oneri",
                due_date=due_date,
                created_at=self._clock.now(),
            )
            actions.add_history(new_id, old=None, new="oneri", by=assignee_id, note=None)
            return new_id

    def plan(self, action_id: int, by_user: int, note: Optional[str] = None):
        with self._uow() as s:
            actions = self._action_repo_factory(s)
            a = actions.get_for_update(action_id)
            assert a.state == "oneri", "Invalid transition"
            actions.update_state(action_id, "planli")
            actions.add_history(action_id, old=a.state, new="planli", by=by_user, note=note)

    def complete(self, action_id: int, by_user: int, note: Optional[str] = None):
        with self._uow() as s:
            actions = self._action_repo_factory(s)
            a = actions.get_for_update(action_id)
            assert a.state == "planli", "Invalid transition"
            actions.update_state(action_id, "tamamlanmis", closed_at=None)
            actions.add_history(action_id, old=a.state, new="tamamlanmis", by=by_user, note=note)

    def close(self, action_id: int, by_user: int, approved: bool, note: Optional[str] = None):
        with self._uow() as s:
            actions = self._action_repo_factory(s)
            a = actions.get_for_update(action_id)
            assert a.state == "tamamlanmis", "Invalid transition"

            new_state = "kapali_onay" if approved else "kapali_red"
            actions.update_state(action_id, new_state, closed_at=self._clock.now())
            actions.add_history(action_id, old=a.state, new=new_state, by=by_user, note=note)

            if not approved:
                # otomatik V2
                v2_id = actions.insert(
                    rc_id=a.rc_id,
                    assignee_id=a.assignee_id,
                    state="oneri",
                    due_date=a.due_date,
                    created_at=self._clock.now(),
                )
                actions.add_history(v2_id, old=None, new="oneri", by=by_user, note="Auto V2")
                return {"closed": action_id, "v2": v2_id}

            return {"closed": action_id}
