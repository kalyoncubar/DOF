# seed/seed_departments.py
from sqlalchemy import (
    MetaData, Table, Column,
    BigInteger, Integer, String, Boolean,
    select, insert
)
from sqlalchemy.engine import Engine
from sqlalchemy import inspect
from config.db import engine

SEED_DEPARTMENTS = [
    {"name": "Üretim", "is_active": True},
    {"name": "Kalite", "is_active": True},
    {"name": "Bakım", "is_active": True},
    {"name": "Satınalma", "is_active": True},
    {"name": "IT", "is_active": True},
]

def _ensure_departments_table(engine: Engine) -> Table:
    md = MetaData()
    insp = inspect(engine)
    # Standart isim: departments
    if not insp.has_table("departments"):
        # Tablonun şemasını oluştur
        tbl = Table(
            "departments", md,
            Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True),
            Column("name", String(128), nullable=False, unique=True),
            Column("is_active", Boolean, nullable=False, default=True),
        )
        md.create_all(engine)
        return tbl
    # Varsa reflekte et
    md.reflect(engine, only=["departments"])
    return md.tables["departments"]

def seed_departments():
    created, skipped = 0, 0
    dept = _ensure_departments_table(engine)
    name_col = dept.c["name"]
    with engine.begin() as conn:
        for d in SEED_DEPARTMENTS:
            exists = conn.execute(select(dept).where(name_col == d["name"])).first()
            if exists:
                skipped += 1
                continue
            conn.execute(insert(dept).values(name=d["name"], is_active=d["is_active"]))
            created += 1
    return {"created": created, "skipped": skipped}

if __name__ == "__main__":
    print(seed_departments())
