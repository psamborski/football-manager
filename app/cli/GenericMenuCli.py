from app.cli.BaseCli import BaseCli


class GenericMenuCli(BaseCli):
    def __init__(self, menu_items=None, prompt="", breadcrumbs=""):
        """
        Initializes the base menu.
        :param menu_items: List of menu items (optional).
        :param prompt: Menu header.
        """
        super().__init__()
        self.menu_items = menu_items or []
        self.breadcrumbs = breadcrumbs
        self.prompt = prompt

    def handle_choice(self, choice):
        """
        Handles user choices. Must be implemented in subclasses.
        :param choice: Selected option.
        """
        raise NotImplementedError("Subclasses must implement `handle_choice`.")

    def run(self):
        """
        Runs the menu in a loop.
        """
        while True:
            choice = self.display_menu(self.menu_items, self.prompt, self.breadcrumbs)
            if not self.handle_choice(choice):
                break