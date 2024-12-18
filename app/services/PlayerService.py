from app.resources.PlayerResource import PlayerResource
from app.models.PlayerModel import PlayerModel
from app.utils import reformat_player_data_from_db


class PlayerService:
    @staticmethod
    def get_top_players_from_country(country_id, limit=100):
        raw_players = PlayerResource.get_players_by_country(country_id, limit, order_by="skill_rating DESC")

        return [
            PlayerModel(
                **reformat_player_data_from_db(player)
            ) for player in raw_players
        ]