from app.cli._GenericViews.ClubSingleView import ClubSingleView


class ExploreSingleClubCli(ClubSingleView):
    def __init__(self, club, clubs_league):
        self.clubs_league = clubs_league
        self.club = club

        super().__init__(
            club=self.club,
            prompt=f"Players from {self.club.name}",
            breadcrumbs=f"Main menu > Explore database > Leagues > {self.clubs_league.name} > {self.club.name}"
        )
