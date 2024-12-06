from random import random, randint

from .TeamModel import Team

class Match:
    def __init__(self, hosts_team: Team, guests_team: Team):
        self.host_team = hosts_team
        self.guest_team = guests_team
        self.score = {hosts_team.team_id: 0, guests_team.team_id: 0}
        self.match_time = 90

    def play_match(self):
        time_remaining = self.match_time

        # update score every 15 mins
        segment_time = 15

        while time_remaining > 0:
            self._play_segment(self.match_time - time_remaining, segment_time)
            time_remaining -= 15


    def _play_segment(self, current_time: int, segment_duration: int):
        # Generate score for current match segment

        if_hosts_scored, hosts_goal_time = self._attempt_goal(self.host_team, current_time, segment_duration)
        if_guests_scored, guests_goal_time = self._attempt_goal(self.guest_team, current_time, segment_duration)

        if if_hosts_scored:
            # print(f'GOAL for {self.host_team.name} ({hosts_goal_time} min)')
            self.score[self.host_team.team_id] += 1

        if if_guests_scored:
            # print(f'GOAL for {self.guest_team.name} ({guests_goal_time} min)')
            self.score[self.guest_team.team_id] += 1


    def _attempt_goal(self, team, current_time, segment_duration):
        # Check if given team scored during given match segment

        probability = team.team_power / (self.host_team.team_power + self.guest_team.team_power)

        # random float between 0 and 1 that makes score less predictable
        randomizer = random()

        # if some team already scored, scoring next goal becomes less and less probable
        randomizer += sum(self.score.values()) / 7   # int in division has been chosen randomly

        # if you're hosts, it's easier for you to score (float below is also random)
        randomizer -= 0.15 if team == self.host_team else 0
        
        if randomizer < probability:
            return True, self._pick_goal_time(current_time, segment_duration)
        else:
            return False, 0


    @staticmethod
    def _pick_goal_time(current_time, segment_duration):
        # Generate match minute in which goal was scored
         return randint(current_time, current_time + segment_duration)


    def __str__(self):
        return f'{self.host_team.name} {self.score[self.host_team.team_id]} - {self.score[self.guest_team.team_id]} {self.guest_team.name}'