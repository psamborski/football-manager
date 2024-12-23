from app.cli.PlayFriendlyMatch.ChooseGuestsLeagueCli import ChooseGuestsLeagueCli
from app.cli._GenericViews.LeagueSingleView import LeagueSingleView


class ChooseHostsClubCli(LeagueSingleView):
    def __init__(self, league):
        self.league = league

        super().__init__(
            league=self.league,
            prompt=f"Choose hosts:",
            breadcrumbs=f"Main menu > Play friendly match"
        )

    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.league_clubs):
            return False  # NoneType = user pressed "q"
        ChooseGuestsLeagueCli(self.league_clubs[choice]).run()
        # return True - going back resets choosing teams
