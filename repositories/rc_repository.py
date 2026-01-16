# repositories/rc_repository.py
from sqlalchemy import (
    MetaData, Table, Column,
    BigInteger, Integer, String, DateTime, ForeignKey,
    select, insert, delete
)
from sqlalchemy import inspect

class RCRepository:
    """
    Core tabanlı repo: 'rc' tablosunu yoksa oluşturur.
    Kolonlar: id, from_comment_id (nullable), created_by, status('open'|'closed'), created_at
    """
    def __init__(self, session):
        self.s = session
        self.engine = session.get_bind()
        self.table = self._ensure_table()

    def _ensure_table(self) -> Table:
        md = MetaData()
        insp = inspect(self.engine)
        if not insp.has_table("rc"):
            tbl = Table(
                "rc", md,
                Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True),
                Column("from_comment_id", BigInteger().with_variant(Integer, "sqlite"), nullable=True),
                Column("created_by", BigInteger().with_variant(Integer, "sqlite"), nullable=False),
                Column("status", String(16), nullable=False),  # 'open' | 'closed'
                Column("created_at", DateTime(timezone=False), nullable=False),
            )
        else:
            md.reflect(self.engine, only=["rc"])
            tbl = md.tables["rc"]
        md.create_all(self.engine)
        return tbl

    def exists(self, rc_id: int) -> bool:
        row = self.s.execute(select(self.table.c.id).where(self.table.c.id == rc_id)).first()
        return bool(row)

    def create(self, from_comment_id: int | None, created_by: int, created_at) -> int:
        self.s.execute(insert(self.table).values(
            from_comment_id=from_comment_id,
            created_by=created_by,
            status="open",
            created_at=created_at,
        ))
        self.s.flush()
        row = self.s.execute(select(self.table.c.id).order_by(self.table.c.id.desc())).first()
        return row[0]

    def delete(self, rc_id: int):
        self.s.execute(delete(self.table).where(self.table.c.id == rc_id))
