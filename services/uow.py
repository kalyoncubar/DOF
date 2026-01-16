# services/uow.py
from contextlib import contextmanager

class UnitOfWork:
    def __init__(self, SessionFactory):
        self._sf = SessionFactory

    @contextmanager
    def __call__(self):
        s = self._sf()
        try:
            yield s
            s.commit()
        except Exception:
            s.rollback()
            raise
        finally:
            s.close()
