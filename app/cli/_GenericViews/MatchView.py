from app.cli.GenericTextCli import GenericTextCli

from app.services.MatchService import MatchService


class MatchView(GenericTextCli):
    def __init__(self, hosts_club, guests_club, prompt="", breadcrumbs=""):
        self.hosts_club = hosts_club
        self.guests_club = guests_club
        self.prompt = prompt
        self.breadcrumbs = breadcrumbs

        self.match = MatchService(
            hosts_club=self.hosts_club,
            guests_club=self.guests_club
        )

        self.match.play_match()

        super().__init__(
            text=repr(self.match),
            prompt=self.prompt,
            breadcrumbs=self.breadcrumbs
        )

    def handle_continue(self):
        pass
