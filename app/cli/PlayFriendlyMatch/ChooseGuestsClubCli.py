from app.cli._GenericViews.LeagueSingleView import LeagueSingleView
from app.cli._GenericViews.MatchView import MatchView
from app.services.ClubService import ClubService


class ChooseGuestsClubCli(LeagueSingleView):
    def __init__(self, league, hosts_club):
        self.league = league
        self.hosts_club = hosts_club

        super().__init__(
            league=self.league,
            prompt=f"Choose guests vs {self.hosts_club.name}:",
            breadcrumbs=f"Main menu > Play friendly match"
        )

    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.league_clubs):
            return False  # NoneType = user pressed "q"
        MatchView(hosts_club=ClubService(self.hosts_club), guests_club=ClubService(self.league_clubs[choice])).run()
        # return True - going back resets choosing teams

