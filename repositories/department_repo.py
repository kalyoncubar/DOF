from models.department import Department
from repositories.base_repo import BaseRepository


class DepartmentRepository(BaseRepository):

    def get_active(self):
        return [d for d in self._items if d.is_active]

    def get_by_name(self, name: str):
        for d in self._items:
            if d.name.lower() == name.lower():
                return d
        return None
