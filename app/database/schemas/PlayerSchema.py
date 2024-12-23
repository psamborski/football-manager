from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class PlayerSchema(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    height = Column(Integer, CheckConstraint('height > 0 AND height < 300'), nullable=False)  # in centimeters
    weight = Column(Float, CheckConstraint('weight > 0 AND weight < 300'), nullable=False)  # in kg
    birthday = Column(Date)
    position = Column(String(50), nullable=False)
    skill_rating = Column(Integer, CheckConstraint('skill_rating > 0 AND skill_rating < 100'), nullable=False)

    # relations with clubs and countries tables
    club_id = Column(Integer, ForeignKey('clubs.club_id'), nullable=True)
    country_id = Column(Integer, ForeignKey('countries.country_id'), nullable=False)

    # orm backrefs to other tables
    club = relationship('ClubSchema', back_populates='players')
    country = relationship('CountrySchema', back_populates='players')


    def __repr__(self):
        return f"<Player(player_id={self.player_id}, name='{self.name}', height={self.height}, weight={self.weight}, birthday={self.birthday}, position='{self.position}', skill_rating={self.skill_rating})>"