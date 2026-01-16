# seed/seed_settings.py
from sqlalchemy import (
    MetaData, Table, Column, String,
    select, insert, update
)
from sqlalchemy.engine import Engine
from sqlalchemy import inspect
from config.db import engine

SEED_SETTINGS = {
    "discussion_threshold": "5",
    "score_nc_open": "2",
    "score_rc_open": "3",
    "score_action_create": "1",
    "score_action_on_time": "5",
    "score_action_delay": "-3",
}

def _ensure_settings_table(engine: Engine) -> Table:
    md = MetaData()
    insp = inspect(engine)
    if not insp.has_table("settings"):
        settings = Table(
            "settings", md,
            Column("key", String(64), primary_key=True),
            Column("value", String(4000), nullable=True),
        )
    else:
        md.reflect(engine, only=["settings"])
        settings = md.tables["settings"]
    md.create_all(engine)
    return settings

def seed_settings():
    created, updated = 0, 0
    settings = _ensure_settings_table(engine)
    with engine.begin() as conn:
        for k, v in SEED_SETTINGS.items():
            exists = conn.execute(select(settings.c.key).where(settings.c.key == k)).first()
            if exists:
                conn.execute(
                    update(settings).where(settings.c.key == k).values(value=v)
                )
                updated += 1
            else:
                conn.execute(insert(settings).values(key=k, value=v))
                created += 1
    return {"created": created, "updated": updated}

if __name__ == "__main__":
    print(seed_settings())
