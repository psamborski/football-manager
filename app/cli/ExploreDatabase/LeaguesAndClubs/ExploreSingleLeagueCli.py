from app.cli.ExploreDatabase.LeaguesAndClubs.ExploreSingleClubCli import ExploreSingleClubCli
from app.cli._GenericViews.LeagueSingleView import LeagueSingleView


class ExploreSingleLeagueCli(LeagueSingleView):
    def __init__(self, league):
        self.league = league

        super().__init__(
            league=self.league,
            prompt=f"Clubs from {self.league.name}",
            breadcrumbs=f"Main menu > Explore database > Leagues > {self.league.name}"
        )

    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.league_clubs):
            return False  # NoneType = user pressed "q"
        ExploreSingleClubCli(self.league_clubs[choice], self.league).run()
