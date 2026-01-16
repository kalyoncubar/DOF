# repositories/user_repository.py
from sqlalchemy.orm import Session
from models.user import User

class UserRepository:
    def __init__(self, s: Session):
        self.s = s

    def exists_active(self, user_id: int) -> bool:
        return (
            self.s.query(User.id)
            .filter(User.id == user_id, User.is_active == True)
            .first()
            is not None
        )

    def get_by_user_code(self, user_code: str) -> dict | None:
        u = (
            self.s.query(User)
            .filter(User.user_code == user_code)
            .first()
        )
        if not u:
            return None
        # auth_routes login için ihtiyaç duyulan alanları döndürüyoruz
        return {
            "id": u.id,
            "user_code": u.user_code,
            "name": u.name,
            "email": u.email,
            "password_hash": u.password_hash,
            "role": u.role,
            "is_active": u.is_active,
        }
