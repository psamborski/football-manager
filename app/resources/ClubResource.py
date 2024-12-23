from sqlalchemy.orm import Session

from app.database.schemas.ClubSchema import ClubSchema
from app.resources.utils import validate_order_by_param, validate_limit_param


class ClubResource:
    """Handles database operations related to Club entities.

    This class allows for retrieving, creating, and deleting club entities 
    within the database, as well as fetching clubs based on specific filters.
    """

    def __init__(self, db_session: Session):
        """Initialize the ClubResource with a database session."""
        self.db_session = db_session

    def get_all_clubs(self, limit=None, order_by=None):
        """Retrieve all clubs from the database.

        Args:
            limit (int, optional): The maximum number of clubs to retrieve.
            order_by (str, optional): Column name to order the results by.

        Returns:
            List[ClubSchema]: A list of club records.
        """
        query = self.db_session.query(ClubSchema)

        if validate_order_by_param(order_by):
            query = query.order_by(order_by)
        if validate_limit_param(limit):
            query = query.limit(limit)

        return query.all()

    def get_club_by_id(self, club_id: int):
        """Retrieve a single club by its ID.

        Args:
            club_id (int): The ID of the club to retrieve.

        Returns:
            ClubSchema or None: The club record if found, else None.
        """
        return self.db_session.query(ClubSchema).filter_by(club_id=club_id).first()

    def get_clubs_by_league_id(self, league_id: int, limit=None, order_by=None):
        """Retrieve clubs belonging to a specific league.

        Args:
            league_id (int): The ID of the league to filter clubs by.
            limit (int, optional): The maximum number of clubs to retrieve.
            order_by (str, optional): Column name to order the results by.

        Returns:
            List[ClubSchema]: A list of club records.
        """
        query = self.db_session.query(ClubSchema).filter_by(league_id=league_id)

        if validate_order_by_param(order_by):
            query = query.order_by(order_by)
        if validate_limit_param(limit):
            query = query.limit(limit)

        return query.all()

    def create_club(self, club_data: dict):
        """Create a new club in the database.

        Args:
            club_data (dict): A dictionary of club data to create the new club.

        Returns:
            ClubSchema: The newly created club record.
        """
        new_club = ClubSchema(**club_data)
        self.db_session.add(new_club)
        self.db_session.commit()
        return new_club

    def delete_club(self, club_id: int):
        """Delete a club from the database.

        Args:
            club_id (int): The ID of the club to delete.

        Returns:
            ClubSchema or None: The deleted club record if found and deleted, else None.
        """
        club = self.get_club_by_id(club_id)
        if club:
            self.db_session.delete(club)
            self.db_session.commit()
        return club
