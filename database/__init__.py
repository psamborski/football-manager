from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Load all schemas so Base can register them and database can work. Order is important!
from .schemas.ClubSchema import ClubSchema
from .schemas.CountrySchema import CountrySchema
from .schemas.LeagueSchema import LeagueSchema
from .schemas.PlayerSchema import PlayerSchema
