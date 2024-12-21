from app.cli.ExploreDatabase.LeaguesAndClubs.ExploreSingleLeagueCli import ExploreSingleLeagueCli
from app.cli._GenericViews.LeagueAllView import LeagueAllView


class ExploreAllLeaguesCli(LeagueAllView):
    def __init__(self):
        super().__init__(
            prompt="Choose league to view its clubs.",
            breadcrumbs="Main menu > Explore database > Leagues"
        )

    # overwrite generic func
    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.leagues_data):
            return False  # NoneType = user pressed "q"
        ExploreSingleLeagueCli(self.leagues_data[choice]).run()
        return True
