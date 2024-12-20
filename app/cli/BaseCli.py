import curses

from config import APP_NAME, APP_VERSION


class BaseCli:
    """
    Core class for managing CLI display and user interaction in this application.

    Features:
        - Handles dynamic menu rendering and scrollable content display.
        - Configures terminal properties like screen size, colors, and cursor visibility.
        - Includes navigation handling and UI elements like breadcrumbs and prompts.
    """
    # Represents the main curses screen buffer for rendering terminal UI components.
    stdscr = None

    @classmethod
    def set_stdscr(cls, stdscr):
        """
        Sets the curses screen buffer to be used for drawing the UI. Inherited by GenericMenuCli and all its subclasses.
        """
        cls.stdscr = stdscr

    def __init__(self):
        """
        Initializes the CLI application and configures essential UI properties like dimensions.
        """
        self.init_colors()  # Initialize terminal colors for colorful text display.

        self.workspace_width = curses.COLS
        self.workspace_height = curses.LINES - 1  # leave room for app info at the bottom

        self.current_menu_option = 0

    def display_menu(self, menu_items, prompt, breadcrumbs, items_per_page=None):
        """
        Displays a menu and processes user inputs for navigation.

        Behaviour:
            - Renders menu items across pages and allows the user to navigate using arrow keys.
            - Highlights the selected menu option and captures the selection or exit input.
            - Uses prompt and breadcrumbs to provide context about the menu and navigation path.

        Args:
            menu_items: List of menu items to display.
            prompt: Text to display at the top of the menu.
            breadcrumbs: Navigation context for the current menu.
            items_per_page: Optional number of menu items to show per page. Defaults based on available space.

        Returns:
            Index of the selected menu item, or None if exited.
        """
        curses.curs_set(0)  # To disable the cursor
        self.stdscr.clear()  # Preparing screen for new display
        self._reset_current_option()  # reset chosen item to first option whenever screen changes

        if items_per_page is None:
            items_per_page = self.workspace_height - 5  # Adjust max items per page based on height.
            if breadcrumbs:
                items_per_page -= 1  # Reduce items if breadcrumbs are displayed.

        total_items = len(menu_items)  # Total menu items.
        total_pages = (total_items + items_per_page - 1) // items_per_page  # Compute total pages.
        current_page = 0

        while True:
            self.stdscr.clear()  # Clear screen for new menu display.
            self._render_header(prompt, breadcrumbs)  # Render the menu prompt and breadcrumbs.

            # pagination vars
            start_idx = current_page * items_per_page
            end_idx = min(start_idx + items_per_page, total_items)
            offset = 2 if breadcrumbs else 1

            # render proper list
            self._render_paginated_menu_items(menu_items, start_idx, end_idx, self.current_menu_option, offset)

            # add UX message if necessary
            if total_pages > 1:
                self.stdscr.addstr(
                    self.workspace_height - 2, 2,
                    f"{current_page + 1} of{total_pages} (press \"q\" to exit...)",
                    curses.A_DIM
                )

            # add footer
            self._render_footer()

            # arrow navigation
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_menu_option > 0:
                self.current_menu_option -= 1  # Move to the previous menu option.
            elif key == curses.KEY_DOWN and self.current_menu_option < total_items - 1:
                self.current_menu_option += 1  # Move to the next menu option.
            elif key == curses.KEY_RIGHT and current_page < total_pages - 1:
                current_page += 1  # Navigate to the next page.
                self.current_menu_option = current_page * items_per_page  # Update current option.
            elif key == curses.KEY_LEFT and current_page > 0:
                current_page -= 1
                self.current_menu_option = current_page * items_per_page + items_per_page - 1
            elif key == curses.KEY_ENTER or key in [10, 13]:  # 10 and 13 - enter in various envs (Mac, Linux, Windows)
                return self.current_menu_option
            elif key == ord('q'):  # q to go back
                return None

    def display_text(self, text, prompt=None, breadcrumbs=None, continue_message="Press any key to continue..."):
        """
        Displays multiline text on the screen with optional prompt, breadcrumbs, and scrolling functionality.

        Behaviour:
            - Renders text contents within the terminal screen, enabling smooth vertical scrolling (navigating with arrow keys).
            - Optionally displays a prompt and breadcrumbs for context.
            - Provides a footer message to guide the user to continue or exit.

        Args:
            text: The content to render, split into lines for display.
            prompt: An optional header prompt to display at the top of the screen.
            breadcrumbs: Navigation breadcrumbs to show the user's current position in the app.
            continue_message: Message displayed at the bottom to inform the user to proceed or exit.
        """
        curses.curs_set(0)  # Disable cursor visibility for better UX.
        self.stdscr.clear()  # Clear the screen for text display.

        text_lines = text.splitlines()  # Split the text into separate lines.
        available_height = self.workspace_height - 5  # Limit height excluding footer space.
        if breadcrumbs:
            available_height -= 1  # Adjust height for breadcrumbs space.
        if prompt:
            available_height -= 1  # Adjust height for prompt space.

        total_lines = len(text_lines)
        current_line = 0

        while True:
            self.stdscr.clear()

            # add header
            self._render_header(prompt, breadcrumbs)

            # define offset above the text
            offset = 2 if breadcrumbs else 1
            offset += 1 if prompt else 0

            end_line = min(current_line + available_height, total_lines)

            # render proper text
            self._render_scrollable_text(text_lines, current_line, end_line, offset)

            # display continue message
            self.stdscr.addstr(self.workspace_height - 2, 2, continue_message, curses.A_DIM)

            # add footer
            self._render_footer()

            # arrows navigation
            key = self.stdscr.getch()
            if key == curses.KEY_UP and current_line > 0:
                current_line -= 1
            elif key == curses.KEY_DOWN and current_line + available_height < total_lines:
                current_line += 1
            else:  # catch any other key to exit
                break

    def _render_header(self, prompt, breadcrumbs):
        """
        Displays the screen header with a prompt and navigation breadcrumbs.

        Args:
            prompt: The header or title text to display.
            breadcrumbs: Navigation breadcrumbs indicating the user's current screen path.
        """
        line = 0
        if prompt:
            self.stdscr.addstr(line, 0, prompt, curses.A_BOLD)
            line += 1
        if breadcrumbs:
            self.stdscr.addstr(line, 0, breadcrumbs, curses.A_DIM)

    def _render_footer(self):
        """
        Renders the application footer with the app name and version number.
        Ensures the footer remains consistent across all screens.
        """
        footer_y = curses.LINES - 1  # Last line of the screen
        self.stdscr.addstr(footer_y, 0, f'{APP_NAME} v.{APP_VERSION}', curses.color_pair(1))
        self.stdscr.refresh()

    def _render_paginated_menu_items(self, menu_items, start_idx, end_idx, current_option, offset):
        """
        Displays menu options with highlight for the currently selected item.

        Behaviour:
            - Paginates the menu items to fit within the available terminal height.
            - Styles menu options based on their type (e.g., "exit", "back").
            - Dynamically adjusts the display based on the current selection.

        Args:
            menu_items: Full list of all menu options.
            start_idx: Index of the first item to display on the current page.
            end_idx: Index of the last item to display on the current page.
            current_option: Currently selected menu option index.
            offset: Vertical offset to determine where to start rendering in the terminal.
        """
        for idx, item in enumerate(menu_items[start_idx:end_idx]):
            line = idx + offset
            if idx + start_idx == current_option:
                self.stdscr.addstr(line, 2, f'> {item}', curses.A_STANDOUT)
            else:
                style = curses.A_DIM if item.lower() in ["exit", "back"] else curses.A_NORMAL
                self.stdscr.addstr(line, 2, f'  {item}', style)

    def _render_scrollable_text(self, text_lines, start_line, end_line, offset):
        """
        Renders a segment of multiline text as scrollable content on the screen.

        Behaviour:
            - Displays only the visible part of the text based on the current scroll position.
            - Maintains alignment with any headers or prompts using an offset.

        Args:
            text_lines: List of text lines to be displayed.
            start_line: Line index to start rendering from.
            end_line: Line index to stop rendering at.
            offset: Starting vertical position in the terminal for text rendering.
        """
        for idx, line in enumerate(text_lines[start_line:end_line]):
            self.stdscr.addstr(idx + offset, 2, line)

    def _reset_current_option(self):
        """
        Resets the current menu option to the first item.
        """
        self.current_menu_option = 0

    @staticmethod
    def init_colors():
        """
        Configures terminal color pairs for the application's user interface.
        """
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
