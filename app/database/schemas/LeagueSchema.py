from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class LeagueSchema(Base):
    __tablename__ = 'leagues'

    league_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    # orm backrefs to other tables
    clubs = relationship('ClubSchema', back_populates='league')

    def __repr__(self):
        return f"<League(league_id={self.league_id}, name='{self.name}')>"
