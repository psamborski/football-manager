class Team:
    def __init__(self, team_id: str, name: str):
        self.team_id = team_id
        self.name = name
        self.players = set()  # players' objects list

    def __str__(self):
        return f"Team: {self.name}"