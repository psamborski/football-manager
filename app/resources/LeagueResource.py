from sqlalchemy.orm import Session

from app.database.schemas.LeagueSchema import LeagueSchema
from app.resources.utils import validate_order_by_param, validate_limit_param


class LeagueResource:
    """Handles operations related to League entities in the database.

        Methods:
        - get_all_leagues: Retrieve a list of all leagues, with optional filters for limit and order.
        - get_league_by_id: Retrieve a specific league identified by its unique ID.
        - create_league: Add a new league entry to the database.
        - delete_league: Remove an existing league from the database.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_leagues(self, limit=None, order_by=None):
        """Retrieve all leagues from the database.

        Args:
            limit (int, optional): The maximum number of leagues to retrieve.
            order_by (str, optional): An attribute to order the results by.

        Returns:
            list: A list of LeagueSchema objects.
        """
        query = self.db_session.query(LeagueSchema)

        if validate_order_by_param(order_by):
            query = query.order_by(order_by)
        if validate_limit_param(limit):
            query = query.limit(limit)

        return query.all()

    def get_league_by_id(self, league_id: int):
        """Retrieve a single league by its unique ID.

        Args:
            league_id (int): The unique ID of the league to retrieve.

        Returns:
            LeagueSchema or None: The league object if found, otherwise None.
        """
        return self.db_session.query(LeagueSchema).filter_by(league_id=league_id).first()

    def create_league(self, league_data: dict):
        """Create a new league in the database.

        Args:
            league_data (dict): A dictionary containing the league details.
                Example: {'name': 'Premier League', 'country': 'England', ...}

        Returns:
            LeagueSchema: The newly created league object.
        """
        new_league = LeagueSchema(**league_data)
        self.db_session.add(new_league)
        self.db_session.commit()
        return new_league

    def delete_league(self, league_id: int):
        """Delete a league from the database.

        Args:
            league_id (int): The unique ID of the league to delete.

        Returns:
            LeagueSchema or None: The deleted league object if it existed, otherwise None.
        """
        league = self.get_league_by_id(league_id)
        if league:
            self.db_session.delete(league)
            self.db_session.commit()
        return league
