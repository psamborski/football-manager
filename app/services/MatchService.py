import time
from random import random, choices, choice

from .ClubService import ClubService
from .constants import MATCH_EVENTS, OPEN_GOAL_ATTEMPT_EVENTS, FOUL_EVENTS, POSITIONS_CARD_MODIFIERS, \
    POSITIONS_SCORING_MODIFIERS, FREE_KICK_ATTEMPT_GOAL_CHANCES, FOUL_OUTCOME_CHANCES, COMMENTARY_EVENT_TYPES, \
    MATCH_COMMENTS_FOR_EVENTS
from .utils import calculate_choice_weights

HOSTS_ADVANTAGE = 0.1

TEAM_STATS_STRUCTURE = {
    'goal': 0,
    'scorers': [],
    'shot': 0,
    'yellow_card': [],
    'red_card': [],
    'foul': 0,
    'offside': 0,
    'corner_kick': 0,
    'free_kick': 0,
    'penalty_kick': 0,
}

EVENT_TYPES = tuple(MATCH_EVENTS.keys())
TEAMS_LOCAL_IDS = ("hosts_team", "guests_team")

# TO FIX: scorers are sometimes from the opposite teams
# TO DO: morale changes on various events (goal for example)

class MatchService:
    def __init__(self, hosts_club: ClubService, guests_club: ClubService):
        self.match_time = 90
        self.match_events = []

        self.teams = {
            TEAMS_LOCAL_IDS[0]: hosts_club,
            TEAMS_LOCAL_IDS[1]: guests_club,
        }
        self.score = {
            TEAMS_LOCAL_IDS[0]: 0,
            TEAMS_LOCAL_IDS[1]: 0,
        }
        self.morale = {
            TEAMS_LOCAL_IDS[0]: 70,
            TEAMS_LOCAL_IDS[1]: 70,
        }
        self.stats = {
            TEAMS_LOCAL_IDS[0]: {**TEAM_STATS_STRUCTURE},
            TEAMS_LOCAL_IDS[1]: {**TEAM_STATS_STRUCTURE},
        }

    def play_match(self):
        current_minute = 1
        while current_minute <= self.match_time:
            self._simulate_minute(current_minute)
            current_minute += 1

    def display_match_simulation(self):
        print(f"MATCH: {self.teams[TEAMS_LOCAL_IDS[0]].name} vs {self.teams[TEAMS_LOCAL_IDS[1]].name}\n")
        time.sleep(2.5)
        print(choice(MATCH_COMMENTS_FOR_EVENTS['kickoff']))
        time.sleep(2.5)
        print('\n(1\') KICKOFF!\n')
        time.sleep(2.5)
        for event in self.match_events:
            print(f'({event["minute"]}\')'
                  f'{event["team_name"]}: '
                  f'{choice(MATCH_COMMENTS_FOR_EVENTS[event["type"]])}')
            time.sleep(2.5)

        print('\n(90\') END!\n')
        time.sleep(2.5)
        print(f'{self.teams[TEAMS_LOCAL_IDS[0]].name}: {self.score[TEAMS_LOCAL_IDS[0]]} - {self.score[TEAMS_LOCAL_IDS[1]]} {self.teams[TEAMS_LOCAL_IDS[1]].name}')
        print('\nMatch stats:')
        print(f'{self.teams[TEAMS_LOCAL_IDS[0]].name}:')
        for stat, value in self.stats[TEAMS_LOCAL_IDS[0]].items():
            print(f'  {stat}: {value}')
        print(f'{self.teams[TEAMS_LOCAL_IDS[1]].name}:')
        for stat, value in self.stats[TEAMS_LOCAL_IDS[1]].items():
            print(f'  {stat}: {value}')
        print(f'Morale: {self.morale[TEAMS_LOCAL_IDS[0]]} - {self.morale[TEAMS_LOCAL_IDS[1]]}')


    def _simulate_minute(self, minute: int):
        event_type, chosen_team = self._generate_event(minute)

        if event_type:
            self._handle_event(event_type, chosen_team, minute)

    def _generate_event(self, minute: int):
        # Determine if an event occurs and its type
        no_event_chance = 0.83  # Base chance that nothing happens

        # ends of halves are more interesting
        if 35 < minute < 45:
            no_event_chance = 0.78
        elif 80 < minute < 90 or 115 < minute < 120:
            no_event_chance = 0.72

        if random() < no_event_chance:
            return None, None

        host_team_event_weight, guest_team_event_weight = self._calculate_team_event_weights()

        event_type = choices(EVENT_TYPES, weights=[0.6, 0.4])[0]

        chosen_team = choices(
            TEAMS_LOCAL_IDS,
            weights=[host_team_event_weight, guest_team_event_weight]
        )[0]

        # if type of event is negative, it happens to the team that loses the draw
        chosen_team = chosen_team if event_type == "positive" else self._get_opposite_team_local_id(chosen_team)

        return event_type, chosen_team  # need to unpack values

    def _calculate_team_event_weights(self):
        host_team_event_score = (
                self.teams[TEAMS_LOCAL_IDS[0]].club_rating["first_eleven_strength"] / 10  # it's 11*100/10 at max
                + self.morale[TEAMS_LOCAL_IDS[0]]
        )
        guest_team_event_score = (
                self.teams[TEAMS_LOCAL_IDS[1]].club_rating["first_eleven_strength"] / 10  # it's 11*100/10 at max
                + self.morale[TEAMS_LOCAL_IDS[1]]
        )

        host_team_event_weight = HOSTS_ADVANTAGE
        host_team_event_weight += (host_team_event_score / (host_team_event_score + guest_team_event_score))
        # add random modifier in range (-0.25 - 0.25); make sure the result is between 0 and 1
        host_team_event_weight = max(0.0, min(1.0, host_team_event_weight + random() / 2 - 0.25))

        guest_team_event_weight = 1 - host_team_event_weight

        return host_team_event_weight, guest_team_event_weight

    def _handle_event(self, event_type: str, team_local_id: str, minute: int):
        event_functions = {
            "open_goal_attempt": self._handle_open_goal_attempt,
            "morale_boost": self._handle_morale_change_event,
            "morale_drop": lambda x, y: self._handle_morale_change_event(x, y, -10),
            "foul": self._handle_foul_event,
        }

        possible_events = list(MATCH_EVENTS[event_type].keys())
        possible_events_weights = list(MATCH_EVENTS[event_type].values())

        event = choices(possible_events, weights=possible_events_weights)[0]

        # handle event
        event_functions[event](team_local_id, minute)
        
    def _handle_goal(self, team_local_id: str, event_type: str, minute: int):
        scorer = self._pick_scorer(team_local_id)
        self.score[team_local_id] += 1
        self.stats[team_local_id]["scorers"].append(scorer)
        self._increase_stat("goal", team_local_id)
        self._increase_stat("shot", team_local_id)
        self._add_event_to_list(
            event_type=event_type,
            team_local_id=team_local_id,
            minute=minute
        )

    def _handle_open_goal_attempt(self, team_local_id: str, minute: int):
        possible_outcomes = list(OPEN_GOAL_ATTEMPT_EVENTS.keys())
        possible_outcomes_weights = list(OPEN_GOAL_ATTEMPT_EVENTS.values())

        outcome = choices(possible_outcomes, weights=possible_outcomes_weights)[0]

        self._add_event_to_list(
            event_type="open_goal_attempt",
            team_local_id=team_local_id,
            minute=minute)

        if outcome == "goal":
            self._handle_goal(
                team_local_id=team_local_id,
                event_type="open_goal",
                minute=minute
            )
        elif outcome == "offside":
            self._increase_stat(outcome, team_local_id)
            self._add_event_to_list(
                event_type="offside",
                team_local_id=team_local_id,
                minute=minute
            )
        elif outcome == "miss":
            self._increase_stat("shot", team_local_id)
            self._add_event_to_list(
                event_type="miss",
                team_local_id=team_local_id,
                minute=minute
            )
        elif outcome in ["corner_kick", "free_kick", "penalty_kick"]:
            if outcome != "corner_kick":
                self._increase_stat("foul", self._get_opposite_team_local_id(team_local_id))

            self._increase_stat(outcome, team_local_id)
            self._handle_free_kick_attempt(
                free_kick_type=outcome,
                team_local_id=team_local_id,
                minute=minute
            )

    def _handle_free_kick_attempt(self, free_kick_type: str, team_local_id: str, minute: int):
        goal_chance = FREE_KICK_ATTEMPT_GOAL_CHANCES.get(free_kick_type, 0)
        is_goal = choices([True, False], weights=[goal_chance, 1 - goal_chance])[0]

        if is_goal:
            self._handle_goal(
                team_local_id=team_local_id,
                event_type=f'{free_kick_type}_goal',
                minute=minute)
        else:
            self._increase_stat("shot", team_local_id)
            self._add_event_to_list(
                event_type=f'{free_kick_type}_miss',
                team_local_id=team_local_id,
                minute=minute
            )

    def _handle_foul_event(self, team_local_id: str, minute: int):
        self._increase_stat("free_kick", self._get_opposite_team_local_id(team_local_id))
        self._increase_stat("foul", team_local_id)
        self._add_event_to_list(
            event_type="foul",
            team_local_id=team_local_id,
            minute=minute
        )

        possible_cards = list(FOUL_EVENTS.keys())
        possible_cards_weights = list(FOUL_EVENTS.values())

        card = choices(possible_cards, weights=possible_cards_weights)[0]

        if card == "red_card":
            self._handle_card_event(team_local_id, minute, card_color="red")
        elif card == "yellow_card":
            self._handle_card_event(team_local_id, minute, card_color="yellow")
        elif card == "no_card":
            self._add_event_to_list(
                event_type="no_card",
                team_local_id=team_local_id,
                minute=minute
            )

        self._handle_free_kick_attempt(
            free_kick_type=choices(
                list(FOUL_OUTCOME_CHANCES.keys()),
                weights=list(FOUL_OUTCOME_CHANCES.values())
            )[0],
            team_local_id=self._get_opposite_team_local_id(team_local_id),
            minute=minute
        )

    def _handle_card_event(self, team_local_id: str, minute: int, card_color="yellow", card_receiver=None):
        if not card_receiver:
            card_receiver = self._pick_card_receiver(team_local_id)

        if card_color == "red":
            self.morale[team_local_id] -= 10
            self.stats[team_local_id]["red_card"].append(card_receiver)
        elif card_color == "yellow":
            if card_receiver not in self.stats[team_local_id]["yellow_card"]:
                self.morale[team_local_id] -= 5
                self.stats[team_local_id]["yellow_card"].append(card_receiver)
            else:
                self._handle_card_event(team_local_id, minute, card_color="red")
        else:
            raise ValueError("Invalid card color")

        self._add_event_to_list(
            event_type=f"{card_color}_card",
            team_local_id=team_local_id,
            minute=minute
        )

    def _handle_morale_change_event(self, team_local_id: str, minute: int, value=10):
        self.morale[team_local_id] += value
        self._add_event_to_list(
            event_type="morale_boost" if value > 0 else "morale_drop",
            team_local_id=team_local_id,
            minute=minute
        )

    def _add_event_to_list(self, event_type: str, team_local_id: str, minute: int):
        if event_type in COMMENTARY_EVENT_TYPES:
            self.match_events.append({
                "type": event_type,
                "team_local_id": team_local_id,
                "team_name": self.teams[team_local_id].name,
                "minute": minute,
            })
        else:
            raise ValueError(f"Invalid event type: {event_type}")

    def _increase_stat(self, stat_name: str, team_local_id: str):
        if stat_name in list(TEAM_STATS_STRUCTURE.keys()) and type(TEAM_STATS_STRUCTURE.get(stat_name)) == int:
            self.stats[team_local_id][stat_name] += 1
        else:
            raise ValueError(f"Stat is not the type of int: {stat_name}")

    def _pick_scorer(self, team_local_id: str):
        possible_players = self.teams[team_local_id].first_eleven
        possible_players_weights = calculate_choice_weights(
            [POSITIONS_SCORING_MODIFIERS[p.position] for p in possible_players])
        return choices(possible_players, weights=possible_players_weights)[0]

    def _pick_card_receiver(self, team_local_id: str):
        possible_players = self.teams[team_local_id].first_eleven
        possible_players_weights = calculate_choice_weights(
            [POSITIONS_CARD_MODIFIERS[p.position] for p in possible_players])
        return choices(possible_players, weights=possible_players_weights)[0]

    @staticmethod
    def _get_opposite_team_local_id(team_local_id: str):
        return TEAMS_LOCAL_IDS[1 - TEAMS_LOCAL_IDS.index(team_local_id)]
