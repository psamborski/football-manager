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
    "GK": 0.5,
    "RB": 0.5,
    "CB": 0.55,
    "LB": 0.5,
    "CDM": 0.6,
    "RM": 0.7,
    "CM": 0.7,
    "LM": 0.7,
    "RW": 0.9,
    "CAM": 0.85,
    "LW": 0.9,
    "ST": 0.1,
}

POSITIONS_CARD_MODIFIERS = {
    "GK": 0.5,
    "RB": 0.8,
    "CB": 0.95,
    "LB": 0.8,
    "CDM": 0.1,
    "RM": 0.65,
    "CM": 0.85,
    "LM": 0.65,
    "RW": 0.55,
    "CAM": 0.65,
    "LW": 0.55,
    "ST": 0.7,
}

# ALL MATCH RELATED EVENTS
# floats mean probability weight
MATCH_EVENTS = {
    "positive": {
        "open_goal_attempt": 0.8,
        "morale_boost": 0.2,
    },
    "negative": {
        "foul": 0.7,
        "morale_drop": 0.3
    }
}

FOUL_EVENTS = {
    "no_card": 0.5,
    "red_card": 0.1,
    "yellow_card": 0.4,
}

OPEN_GOAL_ATTEMPT_EVENTS = {
    "goal": 0.35,
    "offside": 0.1,
    "corner_kick": 0.2,
    "free_kick": 0.1,
    "penalty_kick": 0.05,
    "miss": 0.25
}

FOUL_OUTCOME_CHANCES = {
    "free_kick": 0.92,
    "penalty_kick": 0.08,
}

FREE_KICK_ATTEMPT_GOAL_CHANCES = {
    "corner_kick": 0.2,
    "free_kick": 0.25,
    "penalty_kick": 0.8,
}

COMMENTARY_EVENT_TYPES = {'free_kick_goal', 'red_card', 'morale_boost', 'foul', 'no_card', 'open_goal',
                          'free_kick_miss', 'yellow_card', 'corner_kick_miss', 'foul', 'open_goal_attempt',
                          'penalty_kick_miss', 'morale_drop', 'miss', 'corner_kick_goal', 'penalty_kick_goal',
                          'offside'}

MATCH_COMMENTS_FOR_EVENTS = {
    'kickoff': [
        "Welcome, everyone, to what promises to be a thrilling match today!",
        "Good afternoon, football fans! We’re all set for a fantastic game here.",
        "Hello and welcome! The atmosphere in the stadium is electric as the teams take the field.",
        "It’s a perfect day for football, and we’re excited to bring you all the action live!",
        "Good evening, and get ready for a showdown between two incredible teams!",
        "The wait is over—kickoff is moments away, and we’re in for a treat today!"
    ],
    'free_kick_goal': [
        "GOAAL!!! What a strike! A magnificent free kick ends up in the back of the net!",
        "GOAAL!!! An incredible goal from a set-piece! Simply unstoppable!",
        "GOAAL!!! The goalkeeper had no chance! It's a perfect free kick!",
        "GOAAL!!! A moment of brilliance from the free kick! The crowd erupts in celebration!",
        "GOAAL!!! A textbook free kick! Straight into the top corner!",
        "GOAAL!!! That's why he's on set-pieces! A stunning free kick goal!"
    ],
    'red_card': [
        "The referee reaches for his pocket... it's a red card! The team is down to 10 men!",
        "A reckless challenge, and the referee has shown the red card!",
        "That's a game-changing decision! A red card for unsportsmanlike behavior!",
        "A shocking foul, and the referee has no hesitation. Off he goes!",
        "A moment of madness leads to a red card! What was he thinking?",
        "The referee makes a bold call! A red card changes everything!"
    ],
    'morale_boost': [
        "The crowd is roaring, lifting the team to push forward with renewed energy!",
        "You can feel the shift in momentum as the players rally together!",
        "A quick pep talk on the pitch seems to have reignited their fighting spirit!",
        "The team's determination is back—they're pressing harder than ever!",
        "The energy on the pitch is electric! They're back in the game!",
        "A surge of confidence sweeps through the team. They're unstoppable now!"
    ],
    'foul': [
        "The referee blows his whistle for a foul. That was a clumsy challenge.",
        "A harsh tackle stops the play. Free kick to the other side.",
        "A physical clash on the pitch, and the referee calls for a foul.",
        "The challenge seemed unnecessary, and the referee steps in to intervene.",
        "That's a blatant foul. The referee has no choice but to stop play.",
        "The foul disrupts the flow of the game. A frustrating moment for the team."
    ],
    'no_card': [
        "The referee has a word but decides not to show a card. Just a warning this time.",
        "The player escapes without a booking. A lucky break there!",
        "The referee keeps his cards in his pocket. Play resumes.",
        "It was close, but the referee opts for leniency. No card given.",
        "The ref shows mercy this time. No card for the offender.",
        "A verbal warning from the referee. They're letting this one slide."
    ],
    'open_goal': [
        "GOAAL!!! What a finish! The goalkeeper was nowhere, and it's an easy tap-in!",
        "GOAAL!!! A fantastic team move ends with an open goal! Clinical execution!",
        "GOAAL!!! They capitalize on the defensive error, and it's an open goal!",
        "GOAAL!!! A golden opportunity converted! The net was wide open!",
        "GOAAL!!! The easiest goal he'll ever score! No one was there to stop him!",
        "GOAAL!!! A gift of a goal! The defense is caught napping!"
    ],
    'free_kick_miss': [
        "The free kick goes just wide of the post. So close!",
        "The ball flies over the crossbar. A wasted opportunity from the set piece.",
        "Aiming for glory, but the free kick misses the target.",
        "The free kick lacked precision, and the chance is gone.",
        "He tried to curl it in, but it doesn't trouble the keeper.",
        "A disappointing effort from the free kick. The wall did its job."
    ],
    'yellow_card': [
        "The referee pulls out the yellow card. A caution for the player.",
        "A late challenge earns the player a booking. It's a yellow card.",
        "That tackle was over the line. The referee shows a yellow card.",
        "A necessary foul, but it comes with a booking. Yellow card issued.",
        "The referee has had enough. A yellow card is shown.",
        "A cynical challenge results in a deserved yellow card."
    ],
    'corner_kick_miss': [
        "The corner is delivered, but no one can connect. The chance goes begging!",
        "A wasted opportunity as the corner kick sails past everyone.",
        "The delivery was poor, and the ball is cleared easily by the defense.",
        "The corner kick fails to find its mark. A missed chance!",
        "A poor corner leads to nothing. They'll be disappointed with that.",
        "The set piece comes to nothing as the defense clears their lines."
    ],
    'open_goal_attempt': [
        "They're breaking through the defense... is this the moment?",
        "The forward charges forward, eyeing the goal... what a chance!",
        "They're setting up for a shot! The crowd holds its breath!",
        "The defense is scrambling as the team pushes for an opening!",
        "A glorious chance in front of goal! Will the defense get back in time?",
        "They're getting close to the goal! The pressure mounts on the opposition."
    ],
    'penalty_kick_miss': [
        "The penalty taker misses! The goalkeeper celebrates the save!",
        "It's wide! The penalty kick goes off target!",
        "The shot hits the woodwork! The chance for a goal slips away!",
        "The penalty lacked power, and the keeper makes an easy save!",
        "An agonizing miss from the spot! The fans can't believe it!",
        "The keeper guesses right and makes a fantastic save!"
    ],
    'morale_drop': [
        "The team looks deflated after that missed chance. Heads are down on the pitch.",
        "You can see the frustration building as the players struggle to find rhythm.",
        "The momentum has shifted, and the team seems out of ideas.",
        "A sense of doubt creeps into their game. They need to regroup quickly.",
        "The players look defeated. They need a spark to get back into this.",
        "A heavy blow to their confidence. The team looks out of sorts."
    ],
    'miss': [
        "Oh, what a chance wasted!",
        "The shot goes wide! The fans groan in disappointment.",
        "An opportunity squandered! That should have been on target.",
        "The striker fails to convert, and the chance is gone.",
        "The crowd can't believe it! That was a sitter!",
        "He'll be replaying that miss in his head all night long."
    ],
    'corner_kick_goal': [
        "GOAAL!!! What a header! The corner kick leads to a spectacular goal!",
        "GOAAL!!! Perfect delivery from the corner, and it's a clinical finish!",
        "GOAAL!!! The set-piece works wonders! A goal straight from the corner!",
        "GOAAL!!! A towering leap and a precise header! A goal from the corner kick!",
        "GOAAL!!! A brilliant team effort culminates in a corner kick goal!",
        "GOAAL!!! The crowd erupts as the corner kick finds the back of the net!"
    ],
    'penalty_kick_goal': [
        "GOAAL!!! Cool, calm, and collected! The penalty taker finds the net!",
        "GOAAL!!! An unstoppable shot from the spot! Goal!",
        "GOAAL!!! The goalkeeper guessed wrong, and it's an easy finish!",
        "GOAAL!!! A confident strike from the penalty spot! No chance for the keeper!",
        "GOAAL!!! He steps up and delivers! A perfectly taken penalty.",
        "GOAAL!!! The pressure doesn't faze him! A goal from the penalty spot!"
    ],
    'offside': [
        "The flag is up! The player is caught offside.",
        "A clever run, but the timing was off. Offside called by the referee.",
        "The attack is stopped as the linesman raises the flag for offside.",
        "A fraction too early, and the offside whistle is blown.",
        "The forward is caught out by the offside trap. Smart defending!",
        "The timing was just off. Another chance goes begging due to offside."
    ]
}

