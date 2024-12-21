from app.cli.GenericMenuCli import GenericMenuCli
from app.cli._GenericViews.PlayerSingleView import PlayerSingleView

from app.services.PlayerService import PlayerService


class PlayerAllView(GenericMenuCli):
    def __init__(self, players_limit=100, prompt="", breadcrumbs=""):
        self.players_limit = players_limit
        self.players = PlayerService.get_all_players(limit=100)
        self.prompt = prompt
        self.breadcrumbs = breadcrumbs

        super().__init__(
            menu_items=[f"{player.name} - OVR {player.skill_rating}" for player in self.players],
            prompt=self.prompt,
            breadcrumbs=self.breadcrumbs
        )

    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.players):
            return False    # NoneType = user pressed "q"
        PlayerSingleView(self.players[choice]).run()

        return True
