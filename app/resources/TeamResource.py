import json

from app.models.TeamModel import Team


class TeamResource:
    def __init__(self):
        self.teams = []

    def load_teams(self):
        # load data
        with open('./dummy/teams.json', 'r') as file:
            teams_data = json.load(file)

        # teams objects
        for team_data in teams_data:
            self.teams.append(
                Team(
                    team_data["team_id"],
                    team_data["name"]
                )
            )

    def get_teams(self):
        if not self.teams:
            self.load_teams()

        return self.teams