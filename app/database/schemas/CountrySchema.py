from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class CountrySchema(Base):
    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    # Backref to Player
    players = relationship('PlayerSchema', back_populates='country')
    # just so I can remember - back_populates='country': country is the same word that i use for relationship var name in players schema
    # (PlayersSchema.py): -> country <- = relationship('Country', back_populates='players')
    # and "Player" is the class name I guess

    def __repr__(self):
        return f"<Country(country_id={self.country_id}, name='{self.name}')>"