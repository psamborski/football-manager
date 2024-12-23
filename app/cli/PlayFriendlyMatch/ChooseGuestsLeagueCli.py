from app.cli.PlayFriendlyMatch.ChooseGuestsClubCli import ChooseGuestsClubCli
from app.cli._GenericViews.LeagueAllView import LeagueAllView


class ChooseGuestsLeagueCli(LeagueAllView):
    def __init__(self, hosts_club):
        self.hosts_club = hosts_club
        super().__init__(
            prompt=f"Choose guests vs {self.hosts_club.name}:",
            breadcrumbs="Main menu > Play friendly match"
        )

    # overwrite generic func
    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.leagues_data):
            return False  # NoneType = user pressed "q"
        ChooseGuestsClubCli(self.leagues_data[choice], self.hosts_club).run()
        # return True - going back resets choosing teams
