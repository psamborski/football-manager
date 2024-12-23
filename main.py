import curses
from app.cli.BaseCli import BaseCli
from app.cli.MainMenu.MainMenuCli import MainMenuCli


def main(stdscr):
    # TODO initialize data mapping for countries (id - name), clubs and so on.
    #  Fetch this data once and then you can store it as constant with option to rebuild data after some changes

    BaseCli.set_stdscr(stdscr)

    app = MainMenuCli()
    app.run()

if __name__ == "__main__":
    curses.wrapper(main)