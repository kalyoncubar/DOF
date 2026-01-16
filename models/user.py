from typing import Optional


class User:
    def __init__(
        self,
        id: int,
        user_code: str,          # "001", "002" ...
        name: str,
        password_hash: str,
        role: str,               # "user" | "admin"
        department_id: int,
        email: Optional[str] = None,
        theme: str = "light",    # light | dark
        is_active: bool = True
    ):
        self.id = id
        self.user_code = user_code
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.department_id = department_id
        self.theme = theme
        self.is_active = is_active

    # ---- Role helpers ----
    def is_admin(self) -> bool:
        return self.role == "admin"

    def is_user(self) -> bool:
        return self.role == "user"

    # ---- Status helpers ----
    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True

    def change_theme(self, theme: str):
        if theme not in ("light", "dark"):
            raise ValueError("Invalid theme")
        self.theme = theme

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_code": self.user_code,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "department_id": self.department_id,
            "theme": self.theme,
            "is_active": self.is_active
        }

