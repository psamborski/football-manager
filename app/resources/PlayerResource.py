from sqlalchemy.orm import Session

from app.database import ClubSchema
from app.database.schemas.PlayerSchema import PlayerSchema
from app.resources.utils import validate_order_by_param, validate_limit_param


class PlayerResource:
    """
    Handles database operations related to Player entities.

    Includes methods for retrieving, creating, and deleting Player records.
    Provides filtering and sorting capabilities.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_players(self, limit=None, order_by=None):
        """
        Retrieve all players from the database.

        :param limit: (Optional) Maximum number of players to return.
        :param order_by: (Optional) The field by which to sort the results.
        :return: List of PlayerSchema objects.
        """
        query = self.db_session.query(PlayerSchema)

        if validate_order_by_param(order_by):
            query = query.order_by(order_by)
        if validate_limit_param(limit):
            query = query.limit(limit)

        return query.all()

    def get_player_by_id(self, player_id: int):
        """Retrieve a single player by their ID."""
        return self.db_session.query(PlayerSchema).filter_by(player_id=player_id).first()

    def get_players_by_country(self, country_id: int, limit=None, order_by=None):
        """
        Retrieve players belonging to a specific country.

        :param country_id: The ID of the country.
        :param limit: (Optional) Maximum number of players to return.
        :param order_by: (Optional) The field to sort the results by.
        :return: List of PlayerSchema objects.
        """
        query = self.db_session.query(PlayerSchema).filter_by(country_id=country_id)

        if validate_order_by_param(order_by):
            query = query.order_by(order_by)
        if validate_limit_param(limit):
            query = query.limit(limit)

        return query.all()

    def get_players_by_club(self, club_id: int, limit=None, order_by=None):
        """
        Retrieve players belonging to a specific club.

        :param club_id: The ID of the club.
        :param limit: (Optional) Maximum number of players to return.
        :param order_by: (Optional) The field to sort the results by.
        :return: List of PlayerSchema objects.
        """
        query = self.db_session.query(PlayerSchema).filter_by(club_id=club_id)
        if validate_order_by_param(order_by):
            query = query.order_by(order_by)
        if validate_limit_param(limit):
            query = query.limit(limit)
        return query.all()

    def get_players_by_league(self, league_id: int, limit=None, order_by=None):
        """
        Retrieve players belonging to clubs in a specific league.

        :param league_id: The ID of the league.
        :param limit: (Optional) Maximum number of players to return.
        :param order_by: (Optional) The field to sort the results by.
        :return: List of PlayerSchema objects.
        """
        query = (
            self.db_session.query(PlayerSchema)
            .join(
                ClubSchema.league_id, isouter=True  # TODO verify
            )
            .filter_by(league_id=league_id)
        )

        if validate_order_by_param(order_by):
            query = query.order_by(order_by)
        if validate_limit_param(limit):
            query = query.limit(limit)

        return query.all()

    def create_player(self, player_data: dict):
        """
        Create a new player in the database.

        :param player_data: A dictionary containing the player's data.
        :return: The created PlayerSchema object.
        """
        # Instantiate a new PlayerSchema object with the provided player data
        new_player = PlayerSchema(**player_data)
        self.db_session.add(new_player)
        self.db_session.commit()
        return new_player

    def delete_player(self, player_id: int):
        """Delete a player from the database."""
        player = self.get_player_by_id(player_id)
        if player:
            self.db_session.delete(player)
            self.db_session.commit()
        return player
