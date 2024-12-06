import json

from app.models.PlayerModel import Player


class PlayerResource:
    def __init__(self):
        self.players = []

    def load_players(self):
        # load data
        with open('../datasets/players.json', 'r') as file:
            players_data = json.load(file)

        # players objects
        for player_data in players_data:
            self.players.append(
                Player(
                    player_data["player_id"],
                    player_data["name"],
                    player_data["position"],
                    player_data["skill_level"],
                    player_data["team_id"],
                )
            )

        # print(f'Players:\n {[str(player) for player in players]}')


    @property
    def get_players(self):
        if not self.players:
            self.load_players()
        return self.players
