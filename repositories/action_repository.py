# repositories/action_repository.py
from sqlalchemy import (
    MetaData, Table, Column,
    BigInteger, Integer, String, DateTime,
    ForeignKey, select, insert, update
)
from sqlalchemy import inspect
from types import SimpleNamespace
from datetime import datetime, timezone

def _utcnow_naive():
    return datetime.now(timezone.utc).replace(tzinfo=None)

class ActionRepository:
    """
    SQLAlchemy Core tabanlı Action repo.
    - 'actions' ve 'action_history' tablolarını yoksa oluşturur
    - FK çözümü için önce 'users' ve 'rc' tablolarını aynı MetaData'ya reflect eder
    """

    def __init__(self, s):
        self.s = s
        self.engine = s.get_bind()
        self.actions, self.history = self._ensure_tables()

    def _ensure_tables(self):
        md = MetaData()
        insp = inspect(self.engine)

        # 1) Referans tablo(lar)ı aynı MetaData'ya al (FK sıralaması için şart)
        to_reflect = []
        for t in ("users", "rc", "actions", "action_history"):
            if insp.has_table(t):
                to_reflect.append(t)
        if to_reflect:
            md.reflect(self.engine, only=to_reflect)

        users_tbl = md.tables.get("users")
        rc_tbl = md.tables.get("rc")

        # 2) actions tablosu
        if "actions" not in md.tables:
            # users/rc mevcutsa gerçek FK koy, yoksa FK'siz kolon oluştur (MVP toleransı)
            fk_user = ForeignKey("users.id") if users_tbl is not None else None
            fk_rc   = ForeignKey("rc.id")    if rc_tbl   is not None else None

            # Column tanımını koşullu FK ile yapmak için küçük yardımcı
            def _col_with_fk(name, fk):
                if fk is None:
                    return Column(name, BigInteger().with_variant(Integer, "sqlite"), nullable=False)
                return Column(name, BigInteger().with_variant(Integer, "sqlite"), fk, nullable=False)

            actions = Table(
                "actions", md,
                Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True),
                _col_with_fk("rc_id", fk_rc),
                _col_with_fk("assignee_id", fk_user),
                Column("state", String(32), nullable=False),           # oneri | planli | tamamlanmis | kapali_onay | kapali_red
                Column("due_date", DateTime(timezone=False), nullable=True),
                Column("created_at", DateTime(timezone=False), nullable=False),
                Column("closed_at", DateTime(timezone=False), nullable=True),
            )
        else:
            actions = md.tables["actions"]

        # 3) action_history tablosu
        if "action_history" not in md.tables:
            history = Table(
                "action_history", md,
                Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True),
                Column("action_id", BigInteger().with_variant(Integer, "sqlite"),
                       ForeignKey("actions.id"), nullable=False),
                Column("old_state", String(32), nullable=True),
                Column("new_state", String(32), nullable=False),
                Column("by_user", BigInteger().with_variant(Integer, "sqlite"), nullable=False),
                Column("note", String(500), nullable=True),
                Column("created_at", DateTime(timezone=False), nullable=False),
            )
        else:
            history = md.tables["action_history"]

        # 4) Oluştur (checkfirst=True default)
        md.create_all(self.engine)
        return actions, history

    # ---------- Commands / Queries ----------

    def insert(self, rc_id, assignee_id, state, due_date, created_at):
        self.s.execute(insert(self.actions).values(
            rc_id=rc_id,
            assignee_id=assignee_id,
            state=state,
            due_date=due_date,
            created_at=created_at,
            closed_at=None,
        ))
        self.s.flush()
        row = self.s.execute(select(self.actions.c.id).order_by(self.actions.c.id.desc())).first()
        return row[0]

    def get_for_update(self, action_id: int):
        row = self.s.execute(select(self.actions).where(self.actions.c.id == action_id)).first()
        if not row:
            raise ValueError("Action not found")
        m = row._mapping
        return SimpleNamespace(
            id=m["id"],
            rc_id=m["rc_id"],
            assignee_id=m["assignee_id"],
            state=m["state"],
            due_date=m["due_date"],
            created_at=m["created_at"],
            closed_at=m["closed_at"],
        )

    def update_state(self, action_id: int, new_state: str, closed_at=None):
        vals = {"state": new_state}
        if closed_at is not None:
            vals["closed_at"] = closed_at
        self.s.execute(
            update(self.actions).where(self.actions.c.id == action_id).values(**vals)
        )

    def add_history(self, action_id: int, old, new, by, note):
        self.s.execute(insert(self.history).values(
            action_id=action_id,
            old_state=old,
            new_state=new,
            by_user=by,
            note=note,
            created_at=_utcnow_naive(),
        ))
