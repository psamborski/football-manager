from app.cli.BaseMenuCli import BaseMenuCli
from app.cli.ExploreDatabase.ExploreDatabaseMenuCli import ExploreDatabaseMenuCli
from config import APP_NAME, APP_VERSION


class MainMenuCli(BaseMenuCli):
    def __init__(self, base_cli):
        super().__init__(
            base_cli,
            menu_items=[
                "Explore database",
                "Creators",
                "Exit",
            ],
            prompt=f"Welcome to {APP_NAME}!"
        )

    def handle_choice(self, choice, stdscr):
        if choice == 0:  # Explore database
            ExploreDatabaseMenuCli(self.base_cli).run(stdscr)
        elif choice == 1:  # Creators
            self.base_cli.display_text(
                stdscr,
                f"{APP_NAME} v.{APP_VERSION}\nCreators: Patryk Samborski",
                prompt="Press any key to return to the menu...",
            )
        elif choice == 2:  # Exit
            self.base_cli.display_text(stdscr, f"Thank you for playing {APP_NAME}!", "")
            return False  # Exit application
        return True