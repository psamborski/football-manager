from app.cli.GenericMenuCli import GenericMenuCli
from app.cli._GenericViews.PlayerSingleView import PlayerSingleView

from app.services.PlayerService import PlayerService


class CountrySingleView(GenericMenuCli):
    def __init__(self, country, players_limit=50, prompt="", breadcrumbs=""):
        self.country = country
        self.players_limit = players_limit
        self.top_players_from_country = PlayerService.get_top_players_from_country(self.country.country_id, limit=self.players_limit)
        self.prompt = prompt
        self.breadcrumbs = breadcrumbs

        super().__init__(
            menu_items=[f"{player.name} - OVR {player.skill_rating}" for player in self.top_players_from_country],
            prompt=self.prompt,
            breadcrumbs=self.breadcrumbs
        )

    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.top_players_from_country):
            return False    # NoneType = user pressed "q"
        PlayerSingleView(self.top_players_from_country[choice]).run()
