import curses
from app.cli.BaseCli import BaseCli

def main(stdscr):
    app = BaseCli()
    app.run_welcome_screen(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)