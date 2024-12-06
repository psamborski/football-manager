import json
from random import randint

from app.models.MatchModel import Match
from app.models.PlayerModel import Player
from app.models.TeamModel import Team
from app.resources.PlayerResource import PlayerResource
from app.resources.TeamResource import TeamResource


def main():
    # load required data
    teams = TeamResource().get_teams()
    players = PlayerResource().get_players()

    # assign players to teams and calculate team power after new signing
    for player in players:
        for team in teams:
            if player.team_id == team.team_id:
                team.players.add(player)
                team.update_team_power()

    # play some match
    match = Match(teams[randint(0, len(teams) - 1)], teams[randint(0, len(teams) - 1)])
    match.play_match()
    print(f'\nMatch: {str(match)}')


if __name__ == "__main__":
     main()
