from app.cli.GenericMenuCli import GenericMenuCli
from app.cli._GenericViews.ClubSingleView import ClubSingleView

from app.services.ClubService import ClubService


class LeagueSingleView(GenericMenuCli):
    def __init__(self, league, prompt="", breadcrumbs=""):
        self.league = league
        self.league_clubs = ClubService.get_clubs_by_league_id(self.league.league_id)
        self.prompt = prompt
        self.breadcrumbs = breadcrumbs

        super().__init__(
            menu_items=[club.name for club in self.league_clubs],
            prompt=self.prompt,
            breadcrumbs=self.breadcrumbs
        )

    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.league_clubs):
            return False    # NoneType = user pressed "q"
        ClubSingleView(self.league_clubs[choice]).run()

        return True
