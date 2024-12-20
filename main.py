import curses
from app.cli.BaseCli import BaseCli
from app.cli.MainMenu.MainMenuCli import MainMenuCli


def main(stdscr):
    BaseCli.set_stdscr(stdscr)

    app = MainMenuCli()
    app.run()

if __name__ == "__main__":
    curses.wrapper(main)