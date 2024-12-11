from app.database.schemas.LeagueSchema import LeagueSchema
from sqlalchemy.orm import Session

class LeagueResource:
    """Handles operations related to League entities in the database."""
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_leagues(self):
        """Retrieve all leagues from the database."""
        return self.db_session.query(LeagueSchema).all()

    def get_league_by_id(self, league_id: int):
        """Retrieve a single league by their ID."""
        return self.db_session.query(LeagueSchema).filter_by(league_id=league_id).first()

    def create_league(self, league_data: dict):
        """Create a new league in the database."""
        new_league = LeagueSchema(**league_data)
        self.db_session.add(new_league)
        self.db_session.commit()
        return new_league

    def delete_league(self, league_id: int):
        """Delete a league from the database."""
        league = self.get_league_by_id(league_id)
        if league:
            self.db_session.delete(league)
            self.db_session.commit()
        return league