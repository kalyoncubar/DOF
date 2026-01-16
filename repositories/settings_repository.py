# repositories/settings_repository.py
from sqlalchemy.orm import Session

class SettingsRepository:
    def __init__(self, s: Session): self.s = s
    def get_int(self, key: str, default: int) -> int:
        row = self.s.execute("SELECT value FROM settings WHERE [key]=:k", {"k": key}).fetchone()
        try:
            return int(row[0]) if row and row[0] is not None else default
        except:  # bozuk veri olursa default
            return default
