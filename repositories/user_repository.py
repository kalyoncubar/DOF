from sqlalchemy import select
# ... (dosyanın mevcut içeriği ve sınıf tanımı)

class UserRepository:
    def __init__(self, s): 
        self.s = s
        # mevcut tablona erişim şeklin nasılsa o kalsın; genelde self.table ile

    # ... mevcut metodların

    def get_by_user_code(self, user_code: str) -> dict | None:
        t = self.table
        row = self.s.execute(select(t).where(t.c.user_code == user_code)).first()
        return dict(row._mapping) if row else None
