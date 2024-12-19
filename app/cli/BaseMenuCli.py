class BaseMenuCli:
    def __init__(self, base_cli, menu_items=None, prompt=""):
        """
        Initializes the base menu.
        :param base_cli: BaseCli instance responsible for display handling.
        :param menu_items: List of menu items (optional).
        :param prompt: Menu header.
        """
        self.base_cli = base_cli
        self.menu_items = menu_items or []
        self.prompt = prompt

    def handle_choice(self, choice, stdscr):
        """
        Handles user choices. Must be implemented in subclasses.
        :param choice: Selected option.
        :param stdscr: Curses screen.
        """
        raise NotImplementedError("Subclasses must implement `handle_choice`.")

    def run(self, stdscr):
        """
        Runs the menu in a loop.
        """
        while True:
            choice = self.base_cli.display_menu(self.menu_items, self.prompt)
            if not self.handle_choice(choice, stdscr):
                break