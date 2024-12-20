class Player:
    def __init__(self, player_id: str, name: str, position: str, skill_level: int, team_id: int = None):
        self.player_id = player_id
        self.name = name
        self.position = position  # 'Goalkeeper', 'Defender', etc.
        self.skill_level = skill_level  # let's say 1-100
        self.team_id = team_id  # team ID he plays for

    def __str__(self):
        return f"{self.name} ({self.position}) - Skill: {self.skill_level}"