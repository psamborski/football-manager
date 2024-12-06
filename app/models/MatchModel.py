from .TeamModel import Team

class Match:
    def __init__(self, hosts_team: Team, guests_team: Team):
        self.host_team = hosts_team
        self.guest_team = guests_team
        self.score = {'hosts_team': 0, 'guests_team': 0}

    def play_match(self):
        hosts_skills = sum([player.skill_level for player in self.host_team.players])
        guests_skills = sum([player.skill_level for player in self.guest_team.players])

        if hosts_skills > guests_skills:
            self.score['hosts_team'] = 3
        else:
            self.score['guests_team'] = 3

    def __str__(self):
        return f'{self.host_team.name} {self.score["hosts_team"]} - {self.score["guests_team"]} {self.guest_team.name}'