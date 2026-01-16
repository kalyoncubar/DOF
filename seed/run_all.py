# seed/run_all.py
from .seed_departments import seed_departments
from .seed_users import seed_users
from .seed_settings import seed_settings

def main():
    r1 = seed_departments()
    r2 = seed_users()
    r3 = seed_settings()
    print({"departments": r1, "users": r2, "settings": r3})

if __name__ == "__main__":
    main()
