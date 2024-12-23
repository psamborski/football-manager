from app.cli.GenericTextCli import GenericTextCli


class PlayerSingleView(GenericTextCli):
    def __init__(self, player, prompt="", breadcrumbs=""):
        self.player = player
        self.prompt = prompt or self.player.name
        self.breadcrumbs = breadcrumbs

        super().__init__(
            text=str(player),
            prompt=self.prompt,
            breadcrumbs=self.breadcrumbs
        )

    def handle_continue(self):
        pass
