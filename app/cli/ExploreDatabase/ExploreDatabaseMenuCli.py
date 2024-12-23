from app.cli.ExploreDatabase.Countries.ExploreAllCountriesCli import ExploreAllCountriesCli
from app.cli.ExploreDatabase.LeaguesAndClubs.ExploreAllLeaguesCli import ExploreAllLeaguesCli
from app.cli.GenericMenuCli import GenericMenuCli
from app.cli._GenericViews.PlayerAllView import PlayerAllView
from config import APP_NAME


class ExploreDatabaseMenuCli(GenericMenuCli):
    def __init__(self):
        super().__init__(
            menu_items=[
                "Players",
                "Leagues and clubs",
                "Countries",
                "Back",
            ],
            prompt=f"Explore {APP_NAME} database",
            breadcrumbs="Main menu > Explore database"
        )

    def handle_choice(self, choice):
        if choice == 0:  # Players
            PlayerAllView(
                prompt="TOP 100 players",
                breadcrumbs="Main menu > Explore database > Players"
            ).run()  # generic view
        elif choice == 1:  # Leagues and clubs
            ExploreAllLeaguesCli().run()  # custom view
        if choice == 2:  # Countries
            ExploreAllCountriesCli().run()  # custom view
        elif choice == 3:  # Back
            return False
        return True
