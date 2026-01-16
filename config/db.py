# config/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Örn: mssql+pyodbc://USER:PASS@SERVER/DB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes
DATABASE_URL = "sqlite:///dev.db"  # İlk çalıştırma için kolaylık; MSSQL URL'iyle değiştirilebilir.

engine = create_engine(DATABASE_URL, future=True)
SessionFactory = sessionmaker(bind=engine, future=True)
