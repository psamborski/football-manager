import logging

from config import setup_logging


def main():
    # Initialize logging
    setup_logging()
    logger = logging.getLogger(__name__)

    # load required data
    # teams = TeamResource().get_teams()
    # players = PlayerResource().get_players()
    #
    # # assign players to teams and calculate team power after new signing
    # for player in players:
    #     for team in teams:
    #         if player.club_id == team.club_id:
    #             team.players.add(player)
    #             team.update_team_power()

    # play some match
    # match = Match(teams[randint(0, len(teams) - 1)], teams[randint(0, len(teams) - 1)])
    # match.play_match()
    # print(f'\nMatch: {str(match)}')

    # launch CLI
    # manager_cli = FootballManagerCLI(teams)
    # curses.wrapper(manager_cli.main_menu)
    # logging.info("Exiting Football Manager CLI...")


if __name__ == "__main__":
    main()
