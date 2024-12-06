from .TeamModel import Team

class Match:
    def __init__(self, hosts_team: Team, guests_team: Team):
        self.host_team = hosts_team
        self.guest_team = guests_team
        self.score = {'hosts_team': 0, 'guests_team': 0}
        self.match_time = 90

    def play_match(self):
        # update score every 15 mins
        while self.match_time > 0:
            self._play_segment()
            self.match_time -= 15


    def _attempt_goal(self, team):
        import random
        probability = team.team_power / (self.host_team.team_power + self.guest_team.team_power)
        return random.random() < probability


    def _play_segment(self):
        if self._attempt_goal(self.host_team):
            self.score['hosts_team'] += 1

        if self._attempt_goal(self.guest_team):
            self.score['guests_team'] += 1


    def __str__(self):
        return f'{self.host_team.name} {self.score["hosts_team"]} - {self.score["guests_team"]} {self.guest_team.name}'