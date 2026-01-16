from datetime import datetime
from typing import Optional


class NC:
    """
    Non-Conformity (Uygunsuzluk)
    """

    STATE_OPEN = "open"
    STATE_CLOSED = "closed"

    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        department_id: int,
        created_by_user_id: int,
        state: str = STATE_OPEN,
        created_at: Optional[datetime] = None,
        closed_at: Optional[datetime] = None
    ):
        self.id = id
        self.title = title
        self.description = description

        self.department_id = department_id
        self.created_by_user_id = created_by_user_id

        self.state = state
        self.created_at = created_at or datetime.utcnow()
        self.closed_at = closed_at

    # ---- State helpers ----
    def is_open(self) -> bool:
        return self.state == self.STATE_OPEN

    def is_closed(self) -> bool:
        return self.state == self.STATE_CLOSED

    def close(self):
        """
        Admin tarafından kapatılır
        (Tüm RC'ler kapalı olmalı – bu kural service katmanında)
        """
        self.state = self.STATE_CLOSED
        self.closed_at = datetime.utcnow()

    def reopen(self):
        """
        Gerekirse admin tekrar açabilir
        """
        self.state = self.STATE_OPEN
        self.closed_at = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "department_id": self.department_id,
            "created_by_user_id": self.created_by_user_id,
            "state": self.state,
            "created_at": self.created_at.isoformat(),
            "closed_at": self.closed_at.isoformat() if self.closed_at else None
        }
