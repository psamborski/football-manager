from app.cli.BaseCli import BaseCli


class GenericTextCli(BaseCli):
    def __init__(
            self,
            text="",
            prompt="",
            breadcrumbs="",
            continue_message="Press any key to continue... (tip: use arrow keys to scroll)"
    ):
        """
        Initializes the base text view.
        :param text: The content of the text to display.
        :param breadcrumbs: Breadcrumb navigation to display at the top.
        :param prompt: Header prompt for the text view.
        :param continue_message: Message displayed at the bottom prompting the user to continue.
        """
        super().__init__()
        self.text = text
        self.prompt = prompt
        self.breadcrumbs = breadcrumbs
        self.continue_message = continue_message

    def handle_continue(self):
        """
        Handles the action after the text is displayed. Must be implemented in subclasses.
        """
        # example -> handling keys for custom behaviour should work
        # LOGGER.info("Continue pressed, exiting...")
        # key = self.stdscr.getch()
        # if key == ord('x'):
        #     LOGGER.info("User pressed 'x', exiting...")

        raise NotImplementedError("Subclasses must implement `handle_continue`.")

    def run(self):
        """
        Runs the text display view.
        """
        self.display_text(
            text=self.text,
            prompt=self.prompt,
            breadcrumbs=self.breadcrumbs,
            continue_message=self.continue_message
        )
        self.handle_continue()