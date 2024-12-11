from app.database.schemas.ClubSchema import ClubSchema
from sqlalchemy.orm import Session

class ClubResource:
    """Handles operations related to Club entities in the database."""
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_clubs(self):
        """Retrieve all clubs from the database."""
        return self.db_session.query(ClubSchema).all()

    def get_club_by_id(self, club_id: int):
        """Retrieve a single club by their ID."""
        return self.db_session.query(ClubSchema).filter_by(club_id=club_id).first()

    def create_club(self, club_data: dict):
        """Create a new club in the database."""
        new_club = ClubSchema(**club_data)
        self.db_session.add(new_club)
        self.db_session.commit()
        return new_club

    def delete_club(self, club_id: int):
        """Delete a club from the database."""
        club = self.get_club_by_id(club_id)
        if club:
            self.db_session.delete(club)
            self.db_session.commit()
        return club