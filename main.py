import json

from app.models.MatchModel import Match
from app.models.PlayerModel import Player
from app.models.TeamModel import Team


def main():
    # load data
    with open('datasets/players.json', 'r') as file:
        players_data = json.load(file)

    with open('datasets/teams.json', 'r') as file:
        teams_data = json.load(file)

    # create teams and players objects
    teams = []
    players = []

    # players objects
    for player_data in players_data:
        players.append(
            Player(
                player_data["player_id"],
                player_data["name"],
                player_data["position"],
                player_data["skill_level"],
                player_data["team_id"],
            )
        )

    print(f'Players:\n {[str(player) for player in players]}')

    # teams objects
    for team_data in teams_data:
        teams.append(
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

    # update teams' power
    for team in teams:
        team.update_team_power()

    # play some match
    match = Match(teams[1], teams[2])
    match.play_match()
    print(f'\nMatch: {str(match)}')


if __name__ == "__main__":
     main()
