from app.database import get_db_session, PlayerSchema
from app.models.PlayerModel import PlayerModel
from app.resources.PlayerResource import PlayerResource
from app.utils import reformat_player_data_from_db


class PlayerService:
    """ PlayerService provides functionality to fetch and process player-related data. """

    @staticmethod
    def get_top_players_from_country(country_id, limit=100):
        """
        Fetch and process the top players from a specific country based on skill rating.

        Args:
            country_id (int): The ID of the country for which players will be fetched.
            limit (int, optional): The maximum number of players to retrieve. Defaults to 100.

        Returns:
            List[PlayerModel]: A list of PlayerModel objects representing the top players
            from the specified country, ordered by skill rating in descending order.
        """
        with get_db_session() as db_session:
            player_resource = PlayerResource(db_session)

            raw_players = player_resource.get_players_by_country(
                country_id, limit, order_by=PlayerSchema.skill_rating.desc()
            )

            return [
                PlayerModel(
                    **reformat_player_data_from_db(player)
                ) for player in raw_players
            ]
