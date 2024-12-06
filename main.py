import curses
import logging
from random import randint

from app.cli.FootballManagerCli import FootballManagerCLI
from app.models.MatchModel import Match
from app.resources.PlayerResource import PlayerResource
from app.resources.TeamResource import TeamResource


def main():
    logging.basicConfig(
        filename='app.log',
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG
    )

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
    # match = Match(teams[randint(0, len(teams) - 1)], teams[randint(0, len(teams) - 1)])
    # match.play_match()
    # print(f'\nMatch: {str(match)}')

    # launch CLI
    manager_cli = FootballManagerCLI(teams)
    curses.wrapper(manager_cli.main_menu)
    logging.info("Exiting Football Manager CLI...")


if __name__ == "__main__":
    main()
