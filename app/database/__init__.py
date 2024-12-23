# 1. Warstwa Bazy Danych (Data Access Layer - DAL)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from contextlib import contextmanager

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Create context manager to use later in app for connecting to db
@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Load all schemas so Base can register them and database can work. Order is important!
from .schemas.ClubSchema import ClubSchema
from .schemas.CountrySchema import CountrySchema
from .schemas.LeagueSchema import LeagueSchema
from .schemas.PlayerSchema import PlayerSchema
