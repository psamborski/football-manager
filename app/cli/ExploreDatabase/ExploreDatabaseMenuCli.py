from app.cli.BaseMenuCli import BaseMenuCli
from app.cli.ExploreDatabase.CountriesMenuCli import CountriesMenuCli
from config import APP_NAME


class ExploreDatabaseMenuCli(BaseMenuCli):
    def __init__(self, base_cli):
        super().__init__(
            base_cli,
            menu_items=[
                # "Players",
                # "Clubs",
                "Countries",
                "Back",
            ],
            prompt=f"Explore {APP_NAME} database"
        )

    def handle_choice(self, choice, stdscr):
        # if choice == 0:  # Players
        #     TopPlayersMenu(self.base_cli).run(stdscr)
        # elif choice == 1:  # Clubs
        #     LeaguesMenu(self.base_cli).run(stdscr)
        if choice == 0:  # Countries
            CountriesMenuCli(self.base_cli).run(stdscr)
        elif choice == 1:  # Back
            return False
        return True