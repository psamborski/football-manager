from app.cli.GenericTextCli import GenericTextCli
from config import APP_NAME, APP_VERSION, LOGGER


class AboutCli(GenericTextCli):
    def __init__(self):
        super().__init__(
            text=f"Full app name: {APP_NAME} v.{APP_VERSION}\nCreators: Patryk Samborski",
            prompt="About FM CLI",
            continue_message="Press any key to return to main menu..."
        )

    def handle_continue(self):
        pass