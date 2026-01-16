# repositories/user_repository.py
from sqlalchemy import MetaData, Table, Column, BigInteger, Integer, String, Boolean, DateTime, inspect, select

class UserRepository:
    def __init__(self, s):
        self.s = s
        self.engine = s.get_bind()
        self.table = self._ensure_table()

    def _ensure_table(self):
        md = MetaData()
        insp = inspect(self.engine)

        if not insp.has_table("users"):
            users = Table(
                "users", md,
                Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True),
                Column("user_code", String(64), nullable=False, unique=True),
                Column("name", String(200), nullable=False),
                Column("email", String(255)),
                Column("password_hash", String(255), nullable=False),
                Column("role", String(16), nullable=False),
                Column("department_id", BigInteger().with_variant(Integer, "sqlite"), nullable=True),
                Column("theme", String(16), nullable=False),
                Column("is_active", Boolean, nullable=False, default=True),
                Column("created_at", DateTime(timezone=False), nullable=False),
            )
        else:
            md.reflect(self.engine, only=["users"])
            users = md.tables["users"]

        md.create_all(self.engine)
        return users

    def exists_active(self, user_id: int) -> bool:
        t = self.table
        row = self.s.execute(
            select(t.c.id).where(t.c.id == user_id, t.c.is_active == True)
        ).first()
        return row is not None

    def get_by_user_code(self, user_code: str) -> dict | None:
        t = self.table
        row = self.s.execute(select(t).where(t.c.user_code == user_code)).first()
        return dict(row._mapping) if row else None
