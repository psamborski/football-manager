from app.cli.About.AboutCli import AboutCli
from app.cli.GenericMenuCli import GenericMenuCli
from app.cli.ExploreDatabase.ExploreDatabaseMenuCli import ExploreDatabaseMenuCli
from app.cli.PlayFriendlyMatch.ChooseHostsLeagueCli import ChooseHostsLeagueCli
from config import APP_NAME


class MainMenuCli(GenericMenuCli):
    def __init__(self):
        super().__init__(
            menu_items=[
                "Play friendly match",
                "Explore database",
                "About",
                "Exit",
            ],
            prompt=f"Welcome to {APP_NAME}!",
            breadcrumbs="Main menu"
        )

    def handle_choice(self, choice):
        if choice == 0:  # Explore database
            ChooseHostsLeagueCli().run()
        if choice == 1:  # Explore database
            ExploreDatabaseMenuCli().run()
        elif choice == 2:  # About
            AboutCli().run()
        elif choice == 3:  # Exit
            self.display_text(f"Thank you for playing {APP_NAME}!", continue_message="Press any key to exit...")
            return False  # Exit application
        return True