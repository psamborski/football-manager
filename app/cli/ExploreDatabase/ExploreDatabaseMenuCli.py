from app.cli.GenericMenuCli import GenericMenuCli
from app.cli.ExploreDatabase.Countries.ExploreAllCountriesCli import ExploreAllCountriesCli
from config import APP_NAME


class ExploreDatabaseMenuCli(GenericMenuCli):
    def __init__(self):
        super().__init__(
            menu_items=[
                # "Players",
                # "Clubs",
                "Countries",
                "Back",
            ],
            prompt=f"Explore {APP_NAME} database",
            breadcrumbs="Main menu > Explore database"
        )

    def handle_choice(self, choice):
        # if choice == 0:  # Players
        #     TopPlayersMenu(self.base_cli).run(stdscr)
        # elif choice == 1:  # Clubs
        #     LeaguesMenu(self.base_cli).run(stdscr)
        if choice == 0:  # Countries
            ExploreAllCountriesCli().run()
        elif choice == 1:  # Back
            return False
        return True