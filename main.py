import curses

from app.cli.BaseCli import BaseCli
from app.cli.MainMenu.MainMenuCli import MainMenuCli
from app.models.ClubModel import ClubModel
from app.services.ClubService import ClubService
from app.services.MatchService import MatchService


def main(stdscr):
    # TODO initialize data mapping for countries (id - name), clubs and so on.
    #  Fetch this data once and then you can store it as constant with option to rebuild data after some changes

    # BaseCli.set_stdscr(stdscr)
    #
    # app = MainMenuCli()
    # app.run()

    team_1 = ClubModel(club_id=3).fetch_data_by_id()
    team_1 = ClubService(team_1)
    team_2 = ClubModel(club_id=4).fetch_data_by_id()
    team_2 = ClubService(team_2)

    match = MatchService(
        hosts_club=team_2,
        guests_club=team_1
    )

    match.play_match()
    match.display_match_simulation()

if __name__ == "__main__":
    # curses.wrapper(main)
    main(None)