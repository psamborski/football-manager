class Team:
    def __init__(self, team_id: str, name: str):
        self.team_id = team_id
        self.name = name
        self.players = set()  # players' objects set
        self.team_power = 0

    def update_team_power(self):
        self.team_power = sum([player.skill_rating for player in self.players])

    def __str__(self):
        return f"Team: {self.name}"