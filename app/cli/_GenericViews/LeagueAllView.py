from app.cli.GenericMenuCli import GenericMenuCli
from app.cli._GenericViews.LeagueSingleView import LeagueSingleView

from app.services.AllLeaguesService import AllLeaguesService


class LeagueAllView(GenericMenuCli):
    def __init__(self, prompt="", breadcrumbs=""):
        self.prompt = prompt
        self.breadcrumbs = breadcrumbs

        self.leagues_data = AllLeaguesService.get_all_leagues()

        super().__init__(
            menu_items=[League.name for League in self.leagues_data],
            prompt=self.prompt,
            breadcrumbs=self.breadcrumbs
        )

    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.leagues_data):
            return False    # NoneType = user pressed "q"
        LeagueSingleView(self.leagues_data[choice]).run()
        return True