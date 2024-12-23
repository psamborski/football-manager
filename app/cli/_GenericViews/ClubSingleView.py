from app.cli.GenericMenuCli import GenericMenuCli
from app.cli._GenericViews.PlayerSingleView import PlayerSingleView

from app.services.AllPlayersService import AllPlayersService


class ClubSingleView(GenericMenuCli):
    def __init__(self, club, prompt="", breadcrumbs=""):
        self.club = club
        self.players_from_club = AllPlayersService.get_players_by_club_id(self.club.club_id)
        self.prompt = prompt
        self.breadcrumbs = breadcrumbs

        super().__init__(
            menu_items=[f"{player.name} - OVR {player.skill_rating}" for player in self.players_from_club],
            prompt=self.prompt,
            breadcrumbs=self.breadcrumbs
        )

    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.players_from_club):
            return False  # NoneType = user pressed "q"
        PlayerSingleView(self.players_from_club[choice]).run()

        return True
