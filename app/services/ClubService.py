from math import floor

from app.models import ClubModel
from app.services.AllPlayersService import AllPlayersService
from app.services.constants import PLAYERS_POSITIONS_GROUPS


class ClubService:
    """
    A service class that encapsulates operations related to a SINGLE club.

    Attributes:
        club_id (int): The unique ID of the club got from the passed model.
        name (str): The name of the club got from the passed model.
        players_models (list[dict]): A list of player data dictionaries, fetched for the club.
        club_rating (dict): A dictionary representing the club's calculated ratings, including:
            - overall_strength (float): The overall calculated strength of the club.
            - overall_strength_to_halves (float): Overall strength rounded to the nearest half.
            - first_eleven_strength (float): The calculated strength for the first eleven players.
            - substitutes_strength (float): The calculated strength for substitute players.

    Methods:
        calculate_first_eleven: Determines the best eleven players for the club based on their skills and predefined formations.
        calculate_club_rating: Calculates the overall strength and ratings of the club on a five-point scale.
    """

    def __init__(self, club_model: ClubModel):
        """
        Initializes the ClubService instance using a club model.

        Args:
            club_model (ClubModel): An instance of ClubModel representing the club data.
        """
        self.club_id = club_model.club_id  # Unique identifier for the club.
        self.name = club_model.name  # The club's name.
        self.players_models = self.fetch_players_data()  # Fetch data for the club's players.

        first_eleven, substitutes = self.calculate_first_eleven()
        self.first_eleven = first_eleven
        self.substitutes = substitutes

        self.club_rating = self.calculate_club_rating()  # Calculate the club's ratings.

    def fetch_players_data(self):
        """
        Fetches data for all players associated with the club.

        Returns:
            list[dict]: A list of PlayerModel objects, each representing a player.
        """
        players_service = AllPlayersService()
        return players_service.get_players_by_club_id(self.club_id)

    def calculate_club_rating(self):
        """
        Calculates the overall strength and ratings of the club on a five-point scale.

        The calculation considers:
            - The skill ratings of the first eleven players.
            - The strength of the substitute players.
            - An age-based modifier to account for optimal team age.

        Returns:
            dict: A dictionary of calculated ratings, including:
                - "overall_strength" (float): The overall calculated strength on a scale of 1 to 5.
                - "overall_strength_to_halves" (float): Overall strength rounded to the nearest half.
                - "first_eleven_strength" (float): Calculated strength for the first eleven players.
                - "substitutes_strength" (float): Calculated strength for the substitutes.
        """
        players = self.players_models

        # Default strength if no players exist
        if not players:
            return {
                "overall_strength": 0,
                "overall_strength_to_halves": 0,
                "first_eleven_strength": 0,
                "substitutes_strength": 0,
                "graphical_club_rating": self._get_graphical_club_rating_repr(0)
            }

        AVG_5_STAR_TRESHOLD = 90  # team with 90 power has 5.0/5 rating
        AVG_1_STAR_TRESHOLD = 45  # team with 45 power still has 1.0/5 rating
        SCALE = 5  # max stars number

        # Sort players by rating (highest to lowest)
        players.sort(key=lambda p: getattr(p, "skill_rating", 0), reverse=True)

        # Calculate strength of the first eleven
        first_eleven_strength = sum(getattr(player, "skill_rating", 0) for player in self.first_eleven) / 11

        # Calculate strength of substitutes
        substitutes_strength = (
            sum(getattr(player, "skill_rating", 0) for player in self.substitutes) / len(self.substitutes)
            if self.substitutes else 0
        )

        # Calculate average age and apply age-based modifier
        # or 26 - some random average age if birthday not present in DB - TODO fix birthdays again
        average_age = sum(getattr(player, "age", 0) or 26 for player in players) / len(players)
        age_modifier = 0
        if 23 <= average_age <= 31:
            age_modifier = 0.02  # Bonus for optimal age
        elif average_age < 23:
            age_modifier = -0.05  # Penalty for too young squad
        elif average_age > 31:
            age_modifier = -0.1  # Penalty for too old squad
        elif average_age == 0:  # probable error
            age_modifier = 0

        # Calculate overall strength
        overall_strength = (
                (first_eleven_strength * 0.7) +
                (substitutes_strength * 0.3) +
                (age_modifier * 100)
        )

        strength = min((overall_strength - AVG_1_STAR_TRESHOLD) / (AVG_5_STAR_TRESHOLD - AVG_1_STAR_TRESHOLD) * SCALE, 5)
        strength_rounded_to_halves = round(strength * 2) / 2

        return {
            "overall_strength": strength,
            "overall_strength_to_halves": strength_rounded_to_halves,
            "first_eleven_strength": first_eleven_strength,
            "substitutes_strength": substitutes_strength,
            "graphical_club_rating": self._get_graphical_club_rating_repr(strength_rounded_to_halves)
        }
    
    def calculate_first_eleven(self):
        """
        Determines the optimal first eleven players for the club based on their skill ratings 
        and predefined default formations.

        The method uses a predefined formation to filter and select players for each position 
        based on their ratings, leaving substitutes in the remaining players list.

        Returns:
            tuple: A tuple containing:
                - first_eleven (list): A list of PlayerModel objects representing the best eleven players.
                - remaining_players (list): A list of PlayerModel objects representing the substitutes.
        """
        default_formation = {
            "goalkeepers": 1,
            "right_backs": 1,
            "left_backs": 1,
            "central_backs": 2,
            "left_midfielders": 1,
            "right_midfielders": 1,
            "central_midfielders": 2,
            "forwards": 2
        }

        first_eleven = []  # List to store the selected players for the first eleven.
        remaining_players = self.players_models  # Start with all players as unselected.

        for formation_position, number_of_players in default_formation.items():
            # Get possible specific player positions for the given formation position.
            possible_specific_positions = PLAYERS_POSITIONS_GROUPS.get(formation_position, dict())

            # Filter players matching the required positions.
            possible_players = list(
                filter(lambda p: p.position in possible_specific_positions.keys(), remaining_players))

            # Sort the players by their skill ratings and scale by the position weight.
            selected_players = sorted(
                possible_players,
                key=lambda p: getattr(p, "skill_rating", 0) * possible_specific_positions.get(p.position, 0.8),
                reverse=True)[:number_of_players]

            # Add the selected players to the first eleven.
            first_eleven.extend(selected_players)

            # Remove the selected players from the remaining player pool.
            remaining_players = [p for p in remaining_players if p not in selected_players]

        # Fill the remaining spots in the first eleven if less than 11 players are selected.
        if len(first_eleven) < 11:
            remaining_players.sort(key=lambda p: getattr(p, "skill_rating", 0), reverse=True)
            first_eleven.extend(remaining_players[:(11 - len(first_eleven))])
            remaining_players = remaining_players[(11 - len(first_eleven)):]

        return first_eleven, remaining_players

    def handle_red_card(self, card_receiver_id):
        self.first_eleven.remove(card_receiver_id)
        self.club_rating = self.calculate_club_rating()

    @staticmethod
    def _get_graphical_club_rating_repr(strength_rounded_to_halves):
        star_symbol = '★'
        half_symbol = '½'
        output = '['
        output += star_symbol * floor(strength_rounded_to_halves)
        output += half_symbol if strength_rounded_to_halves % 1 else ''
        output += ']'
        return output
