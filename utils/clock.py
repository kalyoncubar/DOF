# utils/clock.py
from datetime import datetime, timezone
class Clock:
    def now(self):
        # UTC olarak naive datetime (MSSQL DATETIME2 ile uyum)
        return datetime.now(timezone.utc).replace(tzinfo=None)
