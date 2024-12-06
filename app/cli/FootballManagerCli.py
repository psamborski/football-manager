import curses
import logging
from random import randint

from app.models.MatchModel import Match


class FootballManagerCLI:
    def __init__(self, teams):
        self.teams = teams
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
                    stdscr.addstr(idx + 2, 2, f'  {item}')

            key = stdscr.getch()

            if key == curses.KEY_UP and self.current_option > 0:
                self.current_option -= 1
            elif key == curses.KEY_DOWN and self.current_option < len(menu_items) - 1:
                self.current_option += 1
            # 10, 13 are codes for enter in various environments (win/mac/linux)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return self.current_option

    def play_match(self, stdscr):
        # Step 1: Select home team
        self.current_option = 0
        home_team_index = self.display_menu(
            stdscr,
            self.teams,
            "Choose hosts:"
        )
        home_team = self.teams[home_team_index]

        # Step 2: Select guests team
        self.current_option = 0
        guests_team_index = self.display_menu(
            stdscr,
            [team for idx, team in enumerate(self.teams) if idx != home_team_index],
            "Choose guests:"
        )
        guests_team = self.teams[guests_team_index if guests_team_index < home_team_index else guests_team_index + 1]

        # Simulate Match
        match = Match(home_team, guests_team)
        logging.info(f'Playing match: {str(match)}')
        match.play_match()

        # Display Result
        stdscr.clear()
        stdscr.addstr(0, 0, str(match), curses.A_BOLD)
        stdscr.addstr(3, 0, "Press any key to return to main menu.")
        stdscr.getch()

    def main_menu(self, stdscr):
        menu_items = ["Play Match", "Quit"]

        while True:
            self.current_option = 0
            choice = self.display_menu(stdscr, menu_items, "Welcome to Football Manager 0.1!")

            if choice == 0:  # Play Match
                self.play_match(stdscr)
            elif choice == 1:  # Quit
                break
