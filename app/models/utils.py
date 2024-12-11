def reformat_player_data_from_db(player):return {
        "player_id": player.player_id,
        "name": player.name,
        "position": player.position,
        "skill_rating": player.skill_rating,
        "height": player.height,
        "weight": player.weight,
        "birthday": player.birthday,
        "club_id": player.club_id,
        "country_id": player.country_id,
    }

def reformat_club_data_from_db(club):return {
        "club_id": club.club_id,
        "name": club.name,
        "league_id": club.league_id,
        "players_ids": [player.player_id for player in club.players]
    }

def reformat_country_data_from_db(country):return {
        "country_id": country.country_id,
        "name": country.name,
        "players_ids": [player.player_id for player in country.players]
}

def reformat_league_data_from_db(league):return {
        "league_id": league.league_id,
        "name": league.name,
        "clubs_ids": [club.club_id for club in league.clubs]
}