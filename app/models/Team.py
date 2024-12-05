class Team:
    def __init__(self, team_id: str, name: str):
        self.team_id = team_id
        self.name = name
        # self.players = []  # Lista obiektów Player

    # def add_player(self, player):
    #     if len(self.players) < 11:  # Maksymalnie 11 graczy w drużynie
    #         self.players.append(player)
    #         player.team = self
    #     else:
    #         raise ValueError("Team is full!")

    def __str__(self):
        return f"Team: {self.name}"