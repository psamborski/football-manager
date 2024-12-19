import curses

from app.cli.MainMenu.MainMenuCli import MainMenuCli
from config import APP_NAME, APP_VERSION, LOGGER


class BaseCli:
    """
    A base class for CLI-based applications that provides core functionality for creating 
    interactive text-based user interfaces. It leverages the `curses` library to render menus, 
    display textual information, and handle user input. This class includes methods for 
    displaying scrollable menus, showing text prompts, and initializing terminal color schemes.
    """

    def __init__(self, stdscr):
        """
        Initializes the BaseCli instance and sets up essential attributes and configurations.

        Args:
            stdscr: The standard screen object provided by `curses` to handle terminal display.

        Attributes:
            stdscr: Stores the `curses` terminal screen instance for rendering text and UI elements.
            workspace_width (int): Tracks the current width of the terminal workspace.
            workspace_height (int): Tracks the current height of the terminal workspace, leaving 
                                     space for footer display.
            current_menu_option (int): Tracks the currently selected menu option in menus.
        """
        self.stdscr = stdscr

        self.init_colors() # allow terminal to display colorful text

        self.workspace_width = curses.COLS
        self.workspace_height = curses.LINES - 1  # leave room for app info at the bottom

        self.current_menu_option = 0

    def display_footer(self):
        """
        Displays the application name and version at the bottom of the terminal screen.
        """
        footer_y = curses.LINES - 1  # Last line of the screen
        self.stdscr.addstr(footer_y, 0, f'{APP_NAME} v.{APP_VERSION}', curses.color_pair(1))
        self.stdscr.refresh()

    def display_menu(self, menu_items, prompt, breadcrumbs=None, items_per_page=None):
        """
        Renders and handles a scrollable, paginated menu interface with navigation and selection functionality.

        Args:
            menu_items (list): A list of strings representing the options to display in the menu.
            prompt (str): A message displayed at the top of the menu for user guidance.
            breadcrumbs (str, optional): Contextual navigation information displayed at the bottom of the menu.
                                           This could show the user's location within a hierarchical menu system. 
                                           Defaults to None.
            items_per_page (int, optional): The maximum number of menu items to display on a single page. 
                                            If not provided, this value is calculated dynamically 
                                            based on the terminal's size.

        Behavior:
            - Displays the menu options in a paginated format if the number of items exceeds available space.
            - Highlights the currently selected menu item.
            - Supports navigation via arrow keys (`UP`, `DOWN`) and page navigation (`RIGHT`, `LEFT`).
            - Allows item selection with the `ENTER` key and menu exit with the `q` key.

        Returns:
            int: The index of the selected menu option upon confirmation.
            None: If the user chooses to quit the menu using the `q` key.
        """
        # reset CLI display
        curses.curs_set(0)
        self.stdscr.clear()
        self.reset_current_option()

        if items_per_page is None:
            # Calculate the possible number of items per page dynamically based on terminal size
            items_per_page = self.workspace_height - 5  # Leave room for other texts
            # if breadcrumbs:
            #     items_per_page -= 1  # additional line for breadcrumbs

        total_items = len(menu_items)
        total_pages = (total_items + items_per_page - 1) // items_per_page
        current_page = 0

        while True:
            self.stdscr.erase()  # Clear only the main area, not the footer

            # prompt text
            self.stdscr.addstr(0, 0, prompt, curses.A_BOLD)

            # pagination vars
            start_idx = current_page * items_per_page
            end_idx = min(start_idx + items_per_page, total_items)
            page_items = menu_items[start_idx:end_idx]

            # Display only the current page of items
            for idx, item in enumerate(page_items):
                if idx + start_idx == self.current_menu_option:  # active item
                    self.stdscr.addstr(idx + 2, 2, f'> {item}', curses.A_STANDOUT)
                else:
                    if item.lower() in ["exit", "back"]:  # dim Exit/Back buttons
                        self.stdscr.addstr(idx + 2, 2, f'  {item}', curses.A_DIM)
                    else:
                        self.stdscr.addstr(idx + 2, 2, f'  {item}')

            # Display breadcrumbs and page information at the bottom
            if total_pages > 1:
                self.stdscr.addstr(items_per_page + 3, 4, f"{current_page + 1} of {total_pages} (press \"q\" to back...)", curses.A_DIM)
            # if breadcrumbs:
            #     self.stdscr.addstr(items_per_page + 3, 0, breadcrumbs, curses.A_DIM)

            self.display_footer()  # ensure footer is displayed
            self.stdscr.refresh()

            self.stdscr.refresh()
            key = self.stdscr.getch()

            # keyboard navigation within the page (through menu items)
            if key == curses.KEY_UP and self.current_menu_option > 0:
                self.current_menu_option -= 1
                if self.current_menu_option < start_idx:
                    current_page -= 1
            elif key == curses.KEY_DOWN and self.current_menu_option < total_items - 1:
                self.current_menu_option += 1
                if self.current_menu_option >= end_idx:
                    current_page += 1

            # keyboard page navigation
            elif key == curses.KEY_RIGHT and current_page < total_pages - 1:
                current_page += 1
                self.current_menu_option = current_page * items_per_page
            elif key == curses.KEY_LEFT and current_page > 0:
                current_page -= 1
                self.current_menu_option = current_page * items_per_page + items_per_page - 1

            # catch user's select option
            # 10, 13 are codes for enter in various environments (win/mac/linux)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return self.current_menu_option
            # 'q' for quitting
            elif key == ord('q'):
                return None

    def display_text(self, text, prompt="Press any key to continue..."):
        """
        Displays a block of text in the terminal, followed by a prompt message for user acknowledgment.

        Args:
            text (str): The content to be displayed, where each line is separated by newlines.
            prompt (str, optional): A message displayed below the text to instruct the user to proceed.
                                    Defaults to "Press any key to continue...".

        Behavior:
            - Clears the screen before rendering the text.
            - Ensures that the footer with app information remains visible.
            - Awaits a key press from the user before resuming execution.
        """
        curses.curs_set(0)
        self.stdscr.clear()

        # Displaying text
        for idx, line in enumerate(text.splitlines()):
            self.stdscr.addstr(idx + 1, 2, line)

        self.stdscr.addstr(len(text.splitlines()) + 2, 2, prompt, curses.A_BOLD)
        self.display_footer()  # ensure footer is displayed
        self.stdscr.refresh()
        self.stdscr.getch()

    def run_welcome_screen(self):
        """
        Runs the main menu CLI in a continuous loop, allowing users to make choices 
        until they decide to exit.
        """
        main_menu = MainMenuCli(self)
        main_menu.run(self.stdscr)

    def reset_current_option(self):
        """
        Resets the currently selected menu option to the default value (0).
        """
        self.current_menu_option = 0

    @staticmethod
    def init_colors():
        """
        Sets up terminal text styles using color pairs to enhance the visual appearance of the CLI.
        """
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
