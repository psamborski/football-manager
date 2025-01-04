PLAYERS_POSITIONS = {
    "GK",
    "RB",
    "CB",
    "LB",
    "CDM",
    "CM",
    "CAM",
    "RM",
    "LM",
    "RW",
    "LW",
    "ST",
}

# modifiers for player skill rating in given positions
PLAYERS_POSITIONS_GROUPS = {
    "goalkeepers": {"GK": 1},
    "right_backs": {"RB": 1, "LB": 0.8, "CB": 0.65, "CDM": 0.5},
    "left_backs": {"LB": 1, "RB": 0.8, "CB": 0.65, "CDM": 0.5},
    "central_backs": {"CB": 1, "CDM": 0.75, "LB": 0.6, "RB": 0.6},
    "left_midfielders": {"LM": 1, "LW": 1, "RM": 0.8, "RW": 0.8},
    "right_midfielders": {"RM": 1, "RW": 1, "LM": 0.8, "LW": 0.8},
    "central_midfielders": {"CDM": 1, "CM": 1, "CAM": 1, "CB": 0.5},
    "forwards": {"ST": 1, "CAM": 0.8, "LW": 0.9, "RW": 0.9}
}

POSITIONS_SCORING_MODIFIERS = {
    "GK": 5,
    "RB": 50,
    "CB": 55,
    "LB": 50,
    "CDM": 60,
    "RM": 70,
    "CM": 70,
    "LM": 70,
    "RW": 90,
    "CAM": 85,
    "LW": 90,
    "ST": 100,
}

POSITIONS_CARD_MODIFIERS = {
    "GK": 5,
    "RB": 80,
    "CB": 95,
    "LB": 80,
    "CDM": 100,
    "RM": 65,
    "CM": 85,
    "LM": 65,
    "RW": 55,
    "CAM": 65,
    "LW": 55,
    "ST": 70,
}

# added probability weight
MATCH_EVENTS = {
    "positive": {
        "open_goal_attempt": 0.8,
        "morale_boost": 0.2,
    },
    "negative": {
        "red_card": 0.07,
        "yellow_card": 0.3,
        "foul": 0.5,
        "morale_drop": 0.13
    }
}

OPEN_GOAL_ATTEMPT_EVENTS = {
    "goal": 0.3,
    "offside": 0.1,
    "corner_kick": 0.2,
    "free_kick": 0.1,
    "penalty_kick": 0.05,
    "miss": 0.3
}
