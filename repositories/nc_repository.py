# repositories/nc_repository.py
from sqlalchemy import (
    MetaData, Table, Column,
    BigInteger, Integer, String, DateTime,
    select, insert, update
)
from sqlalchemy import inspect

class NCRepository:
    """
    Core tabanlı repository:
    - Tablonun adı: 'nc' (yoksa oluşturur)
    - Kolonlar: id, title, status('open'|'closed'), opened_by, created_at, closed_by_admin_id, reopened_by_admin_id
    """
    def __init__(self, session):
        self.s = session
        self.engine = session.get_bind()
        self.table = self._ensure_table()

    def _ensure_table(self) -> Table:
        md = MetaData()
        insp = inspect(self.engine)
        if not insp.has_table("nc"):
            tbl = Table(
                "nc", md,
                Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True),
                Column("title", String(200), nullable=False),
                Column("status", String(16), nullable=False),  # 'open' | 'closed'
                Column("opened_by", BigInteger().with_variant(Integer, "sqlite"), nullable=False),
                Column("created_at", DateTime(timezone=False), nullable=False),
                Column("closed_by_admin_id", BigInteger().with_variant(Integer, "sqlite")),
                Column("reopened_by_admin_id", BigInteger().with_variant(Integer, "sqlite")),
            )
        else:
            md.reflect(self.engine, only=["nc"])
            tbl = md.tables["nc"]
        md.create_all(self.engine)
        return tbl

    def get_by_id(self, nc_id: int) -> dict | None:
        row = self.s.execute(select(self.table).where(self.table.c.id == nc_id)).first()
        return dict(row._mapping) if row else None

    def list_all(self) -> list[dict]:
        rows = self.s.execute(select(self.table).order_by(self.table.c.id.desc())).all()
        return [dict(row._mapping) for row in rows]

    def create(self, title: str, opened_by: int, created_at) -> int:
        self.s.execute(insert(self.table).values(
            title=title, status="open", opened_by=opened_by, created_at=created_at
        ))
        self.s.flush()
        # id'yi almak için son kaydı çek (SQLite/MSSQL uyumlu basit yöntem)
        row = self.s.execute(select(self.table.c.id).order_by(self.table.c.id.desc())).first()
        return row[0]

    def set_state(self, nc_id: int, new_state: str, closed_by_admin_id: int | None = None, reopened_by_admin_id: int | None = None):
        values = {"status": new_state}
        if closed_by_admin_id is not None:
            values["closed_by_admin_id"] = closed_by_admin_id
        if reopened_by_admin_id is not None:
            values["reopened_by_admin_id"] = reopened_by_admin_id
        self.s.execute(update(self.table).where(self.table.c.id == nc_id).values(**values))

    def update_title(self, nc_id: int, title: str):
        self.s.execute(update(self.table).where(self.table.c.id == nc_id).values(title=title))
