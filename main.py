import json

from app.models.PlayerModel import Player
from app.models.TeamModel import Team


def main():
    # load data
    with open('mocks/players.json', 'r') as file:
        players_data = json.load(file)

    with open('mocks/teams.json', 'r') as file:
        teams_data = json.load(file)

    # create teams and players objects
    teams = set()
    players = set()

    # players objects
    for player_data in players_data:
        players.add(
            Player(
                player_data["player_id"],
                player_data["name"],
                player_data["position"],
                player_data["skill_level"]
            )
        )

    print(f'Players:\n {[str(player) for player in players]}')

    # teams objects
    for team_data in teams_data:
        teams.add(
            Team(
                team_data["team_id"],
                team_data["name"]
            )
        )

    # assign players to teams
    for player in players:
        for team in teams:
            if player.team_id == team.team_id:
                team.players.add(player)

    print(f'Teams:\n {[str(team) for team in teams]}')


if __name__ == "__main__":
     main()
