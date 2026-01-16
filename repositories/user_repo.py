from models.user import User
from repositories.base_repo import BaseRepository


class UserRepository(BaseRepository):

    def get_by_user_code(self, user_code: str) -> User | None:
        for u in self._items:
            if u.user_code == user_code:
                return u
        return None

    def get_active_users(self):
        return [u for u in self._items if u.is_active]

    def list_by_department(self, department_id: int):
        return [
            u for u in self._items
            if u.department_id == department_id and u.is_active
        ]
