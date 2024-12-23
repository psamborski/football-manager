from app.cli.PlayFriendlyMatch.ChooseHostsClubCli import ChooseHostsClubCli
from app.cli._GenericViews.LeagueAllView import LeagueAllView


class ChooseHostsLeagueCli(LeagueAllView):
    def __init__(self):
        super().__init__(
            prompt="Choose hosts:",
            breadcrumbs="Main menu > Play friendly match"
        )

    # overwrite generic func
    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.leagues_data):
            return False  # NoneType = user pressed "q"
        ChooseHostsClubCli(self.leagues_data[choice]).run()
        # return True - going back resets choosing teams
