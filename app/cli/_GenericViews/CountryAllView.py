from app.cli.GenericMenuCli import GenericMenuCli
from app.cli._GenericViews.CountrySingleView import CountrySingleView

from app.services.CountryService import CountryService


class CountryAllView(GenericMenuCli):
    def __init__(self, prompt="", breadcrumbs=""):
        self.prompt = prompt
        self.breadcrumbs = breadcrumbs

        self.countries_data = CountryService.get_all_countries()

        super().__init__(
            menu_items=[country.name for country in self.countries_data],
            prompt=self.prompt,
            breadcrumbs=self.breadcrumbs
        )

    def handle_choice(self, choice):
        if not isinstance(choice, int) or choice < 0 or choice >= len(self.countries_data):
            return False    # NoneType = user pressed "q"
        CountrySingleView(self.countries_data[choice]).run()
