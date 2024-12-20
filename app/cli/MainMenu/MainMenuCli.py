from app.cli.GenericMenuCli import GenericMenuCli
from app.cli.ExploreDatabase.ExploreDatabaseMenuCli import ExploreDatabaseMenuCli
from config import APP_NAME, APP_VERSION


class MainMenuCli(GenericMenuCli):
    def __init__(self):
        super().__init__(
            menu_items=[
                "Explore database",
                "About",
                "Exit",
            ],
            prompt=f"Welcome to {APP_NAME}!",
            breadcrumbs="Main menu"
        )

    def handle_choice(self, choice):
        if choice == 0:  # Explore database
            ExploreDatabaseMenuCli().run()
        elif choice == 1:  # About
            self.display_text(
                f"Full app name: {APP_NAME} v.{APP_VERSION}\nCreators: Patryk Samborski",
                prompt="About FM CLI",
                continue_message="Press any key to return to main menu..."
            )
        elif choice == 2:  # Exit
            self.display_text(f"Thank you for playing {APP_NAME}!", "")
            return False  # Exit application
        return True