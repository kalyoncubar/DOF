# seed/seed_users.py
from sqlalchemy import (
    MetaData, Table, Column,
    BigInteger, Integer, String, Boolean, DateTime, ForeignKey,
    select, insert
)
from sqlalchemy.engine import Engine
from sqlalchemy import inspect
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

from config.db import engine

# user_code, name, email, role, department_name
SEED_USERS = [
    ("u001", "admin",           "u001@example.com",               "admin", "Kalite"),
    ("u002", "Ozlem Rodoplu",   "ozlem.rodoplu@intergaz.com",     "user",  "Üretim"),
    ("u003", "user3",           "user3@example.com",              "user",  "Bakım"),
    ("u004", "user4",           "user4@example.com",              "user",  "Satınalma"),
    ("u007", "Baris KALYONCU",  "baris.kalyoncu@intergaz.com",    "user",  "IT"),
]

DEFAULT_PASSWORD = "1234"

def _utcnow_naive():
    return datetime.now(timezone.utc).replace(tzinfo=None)

def _ensure_tables(engine: Engine):
    """
    departments ve users tablolarını Core ile garanti altına alır.
    """
    md = MetaData()
    insp = inspect(engine)

    # Departments
    if not insp.has_table("departments"):
        departments = Table(
            "departments", md,
            Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True),
            Column("name", String(128), nullable=False, unique=True),
            Column("is_active", Boolean, nullable=False, default=True),
        )
    else:
        md.reflect(engine, only=["departments"])
        departments = md.tables["departments"]

    # Users
    if not insp.has_table("users"):
        users = Table(
            "users", md,
            Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True),
            Column("user_code", String(64), nullable=False, unique=True),
            Column("name", String(200), nullable=False),
            Column("email", String(255)),
            Column("password_hash", String(255), nullable=False),
            Column("role", String(16), nullable=False),  # 'user' | 'admin' (CHECK constraint migration'da)
            Column("department_id", BigInteger().with_variant(Integer, "sqlite"),
                   ForeignKey("departments.id"), nullable=True),
            Column("theme", String(16), nullable=False, default="light"),
            Column("is_active", Boolean, nullable=False, default=True),
            Column("created_at", DateTime(timezone=False), nullable=False),
        )
    else:
        md.reflect(engine, only=["departments", "users"])
        users = md.tables["users"]
        departments = md.tables["departments"]

    # Tabloları oluştur (varsa no-op)
    md.create_all(engine)
    return users, departments

def _get_department_id_by_name(conn, departments, name: str):
    name_col = departments.c["name"]
    # PK kolonunu belirle
    pk_col = list(departments.primary_key.columns)[0]
    # Yalnızca PK sütununu seç → Row[0] güvenle alınır
    row = conn.execute(select(pk_col).where(name_col == name)).first()
    return row[0] if row else None

def seed_users():
    created, skipped, missing_deps = 0, 0, set()
    users, departments = _ensure_tables(engine)

    with engine.begin() as conn:
        user_code_col = users.c["user_code"]

        for user_code, name, email, role, dep_name in SEED_USERS:
            exists = conn.execute(select(users).where(user_code_col == user_code)).first()
            if exists:
                skipped += 1
                continue

            dep_id = _get_department_id_by_name(conn, departments, dep_name)
            if dep_id is None:
                missing_deps.add(dep_name)
                skipped += 1
                continue

            conn.execute(insert(users).values(
                user_code=user_code,
                name=name,
                email=email,
                role=role,
                department_id=dep_id,
                is_active=True,
                theme="light",
                password_hash=generate_password_hash(DEFAULT_PASSWORD),
                created_at=_utcnow_naive(),
            ))
            created += 1

    return {
        "created": created,
        "skipped": skipped,
        "missing_departments": sorted(missing_deps),
    }

if __name__ == "__main__":
    print(seed_users())

