from app.cli.BaseMenuCli import BaseMenuCli

from app.services.CountryService import CountryService


class CountriesMenuCli(BaseMenuCli):
    def __init__(self, base_cli):
        self.countries_data = CountryService.get_all_countries()

        super().__init__(
            base_cli,
            menu_items=[country.name for country in self.countries_data],
            prompt="Choose country to view its TOP 10 players."
        )

    def handle_choice(self, choice, stdscr):
        pass
        # if choice == 0:  # Players
        #     TopPlayersMenu(self.base_cli).run(stdscr)
        # elif choice == 1:  # Clubs
        #     LeaguesMenu(self.base_cli).run(stdscr)
        # elif choice == 2:  # Countries
        #     CountriesMenu(self.base_cli).run(stdscr)
        # elif choice == 3:  # Back
        #     return False
        # return True
