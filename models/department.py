from typing import Optional


class Department:
    def __init__(
        self,
        id: int,
        name: str,
        is_active: bool = True
    ):
        self.id = id
        self.name = name
        self.is_active = is_active

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }
