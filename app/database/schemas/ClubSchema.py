from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ClubSchema(Base):
    __tablename__ = 'clubs'

    club_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    # relation with league table
    league_id = Column(Integer, ForeignKey('leagues.league_id'), nullable=False)

    # backref to players and leagues
    players = relationship('PlayerSchema', back_populates='club')
    league = relationship('LeagueSchema', back_populates='clubs')

    def __repr__(self):
        return f"<Club(club_id={self.club_id}, name='{self.name}')>"