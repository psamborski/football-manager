from random import random, randint

from .TeamModel import Team


class Match:
    def __init__(self, hosts_team: Team, guests_team: Team):
        self.host_team = hosts_team
        self.guest_team = guests_team
        self.score = {hosts_team.team_id: 0, guests_team.team_id: 0}
        self.match_time = 90
        self.stats = {
            self.host_team.team_id: {
                "scorers": []
            },
            self.guest_team.team_id: {
                "scorers": []
            }
        }

    def play_match(self):
        time_remaining = self.match_time

        # update score every 15 mins
        segment_time = 15

        while time_remaining > 0:
            self._play_segment(self.match_time - time_remaining, segment_time)
            time_remaining -= 15

    def _play_segment(self, current_time: int, segment_duration: int):
        # Generate score for current match segment

        if self._attempt_goal(self.host_team, current_time, segment_duration):
            # print(f'GOAL for {self.host_team.name} ({hosts_goal_time} min)')
            self.score[self.host_team.team_id] += 1

        if self._attempt_goal(self.guest_team, current_time, segment_duration):
            # print(f'GOAL for {self.guest_team.name} ({guests_goal_time} min)')
            self.score[self.guest_team.team_id] += 1

    def _attempt_goal(self, team, current_time, segment_duration):
        # Check if given team scored during given match segment

        probability = team.team_power / (self.host_team.team_power + self.guest_team.team_power)

        # random float between 0 and 1 that makes score less predictable
        randomizer = random()

        # if some team already scored, scoring next goal becomes less and less probable
        randomizer += sum(self.score.values()) / 7  # int in division has been chosen randomly

        # if you're hosts, it's easier for you to score (float below is also random)
        randomizer -= 0.15 if team == self.host_team else 0

        if randomizer < probability:
            # generate scorer and goal time
            self.stats[team.team_id]["scorers"].append(
                [self._pick_scorer(team.players), self._pick_goal_time(current_time, segment_duration)]
            )
            return True
        else:
            return False

    @staticmethod
    def _pick_goal_time(current_time, segment_duration):
        # Generate match minute in which goal was scored
        return randint(current_time, current_time + segment_duration)

    @staticmethod
    def _pick_scorer(players):
        # Generate scorer basing on position and rating
        # The system: player who gets the most points is the scorer. Points are given for rating, position and random modifier
        position_points = {
            'GK': 5,
            'DEF': 50,
            'MID': 80,
            'FWD': 100
        }

        score_chances = []
        for player in players:
            score_points = player.skill_rating
            score_points += position_points[player.position]
            score_points += randint(10, 100)
            score_chances.append([player, score_points])

        return max(score_chances, key=lambda x: x[1])[0]

    def __str__(self):
        return f'{self.host_team.name} {self.score[self.host_team.team_id]} - {self.score[self.guest_team.team_id]} {self.guest_team.name}'

    def __repr__(self):
        scoreboard = ('MATCH:\n'
                      f'{self.host_team.name} {self.score[self.host_team.team_id]}'
                      ' - '
                      f'{self.score[self.guest_team.team_id]} {self.guest_team.name}'
                      )

        for team_id, team_stats in self.stats.items():
            scoreboard += f'\n{self.host_team.name if team_id == self.host_team.team_id else self.guest_team.name}:'
            for scorer in team_stats["scorers"]:
                scoreboard += f'  {scorer[0].name} \'{scorer[1]}'
        return scoreboard
