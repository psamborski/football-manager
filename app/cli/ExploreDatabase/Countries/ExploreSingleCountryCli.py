from app.cli._GenericViews.CountrySingleView import CountrySingleView

from app.services.PlayerService import PlayerService


class ExploreSingleCountryCli(CountrySingleView):
    def __init__(self, country):
        self.country = country
        self.players_limit = 50

        super().__init__(
            country=self.country,
            players_limit=self.players_limit,
            prompt=f"TOP {self.players_limit} players from {self.country.name}",
            breadcrumbs=f"Main menu > Explore database > Countries > {self.country.name}"
        )

    # IMPORTANT no need to overwrite generic function and, accordingly, player view
    # def handle_choice(self, choice):
    #     if not isinstance(choice, int) or choice < 0 or choice >= len(self.top_players_from_country):
    #         return False    # NoneType = user pressed "q"
    #     ExploreSinglePlayerCli(self.top_players_from_country[choice], self.country.name).run()
