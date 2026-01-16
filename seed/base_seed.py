# seed/base_seed.py
from contextlib import contextmanager
from datetime import datetime, timezone

def utcnow_naive():
    return datetime.now(timezone.utc).replace(tzinfo=None)

@contextmanager
def session_scope(SessionFactory):
    s = SessionFactory()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()
