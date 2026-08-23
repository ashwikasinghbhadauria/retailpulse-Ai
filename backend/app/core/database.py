import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.core.config import settings

# Ensure sqlite parent directory exists if using SQLite
if settings.DATABASE_URL.startswith("sqlite"):
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    if "/" in db_path or "\\" in db_path:
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
