# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Usa SQLite por defecto, pero puedes cambiarlo a PostgreSQL en Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./music_app.db")

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()