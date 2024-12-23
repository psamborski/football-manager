from app.cli.GenericMenuCli import GenericMenuCli
from app.cli._GenericViews.ClubSingleView import ClubSingleView

from app.services.AllClubsService import AllClubsService
from app.services.ClubService import ClubService
from config import LOGGER


class LeagueSingleView(GenericMenuCli):
    def __init__(self, league, prompt="", breadcrumbs=""):
        self.league = league
        self.league_clubs = [ClubService(club_model) for club_model in
                             AllClubsService.get_clubs_by_league_id(self.league.league_id)]
        self.prompt = prompt
        self.breadcrumbs = breadcrumbs

        try:
            sdf = [f"{club.name} {club.club_rating.get('graphical_club_rating', '')}" for club in self.league_clubs]
        except Exception as e:
            LOGGER.error(e)
            LOGGER.error([x.club_rating for x in self.league_clubs])

        super().__init__(
            menu_items=[f"{club.name} {club.club_rating.get('graphical_club_rating', '')}" for club in self.league_clubs],
            prompt=self.prompt,
            breadcrumbs=self.breadcrumbs
        )

    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.league_clubs):
            return False  # NoneType = user pressed "q"
        ClubSingleView(self.league_clubs[choice]).run()

        return True
