import curses

from app.cli.MainMenu.MainMenuCli import MainMenuCli


class BaseCli:
    def __init__(self):
        self.current_option = 0

    def display_menu(self, stdscr, menu_items, prompt):
        curses.curs_set(0)
        stdscr.clear()

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, prompt, curses.A_BOLD)

            for idx, item in enumerate(menu_items):
                if idx == self.current_option:
                    # idx + 2, 2 - coordinates y x; left some space for prompt and padding left
                    stdscr.addstr(idx + 2, 2, f'> {item}', curses.A_STANDOUT)

                else:
                    if item == "Exit" or item == "Back":    # mark out Exit and Back button
                        stdscr.addstr(idx + 2, 2, f'  {item}', curses.A_DIM)
                    else:
                        stdscr.addstr(idx + 2, 2, f'  {item}')

            key = stdscr.getch()

            if key == curses.KEY_UP and self.current_option > 0:
                self.current_option -= 1
            elif key == curses.KEY_DOWN and self.current_option < len(menu_items) - 1:
                self.current_option += 1
            # 10, 13 are codes for enter in various environments (win/mac/linux)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return self.current_option

    def display_text(self, stdscr, text, prompt="Press any key to continue..."):
        curses.curs_set(0)
        stdscr.clear()

        # Displaying text
        for idx, line in enumerate(text.splitlines()):
            stdscr.addstr(idx + 1, 2, line)

        stdscr.addstr(len(text.splitlines()) + 2, 2, prompt, curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()

    def run_welcome_screen(self, stdscr):
        """
        Runs main menu in a loop, allowing users to make choices until they choose to exit.
        """
        main_menu = MainMenuCli(self)
        main_menu.run(stdscr)