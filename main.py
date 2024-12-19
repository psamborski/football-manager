import curses
from app.cli.BaseCli import BaseCli

def main(stdscr):
    app = BaseCli(stdscr)
    app.run_welcome_screen()

if __name__ == "__main__":
    curses.wrapper(main)