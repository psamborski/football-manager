from app.cli.ExploreDatabase.Countries.ExploreSingleCountryCli import ExploreSingleCountryCli
from app.cli._GenericViews.CountryAllView import CountryAllView


class ExploreAllCountriesCli(CountryAllView):
    def __init__(self):
        super().__init__(
            prompt="Choose country to view its TOP players.",
            breadcrumbs="Main menu > Explore database > Countries"
        )

    # overwrite generic func
    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.countries_data):
            return False    # NoneType = user pressed "q"
        ExploreSingleCountryCli(self.countries_data[choice]).run()
