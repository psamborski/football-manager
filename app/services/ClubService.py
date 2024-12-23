from math import floor

from app.models import ClubModel
from app.services.AllPlayersService import AllPlayersService


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

        AVG_5_STAR_TRESHOLD = 99
        SCALE = 5  # max stars number

        # Sort players by rating (highest to lowest)
        players.sort(key=lambda p: getattr(p, "skill_rating", 0), reverse=True)

        # Divide players into first eleven and substitutes
        first_eleven = players[:11]
        substitutes = players[11:]

        # Calculate strength of the first eleven
        first_eleven_strength = sum(getattr(player, "skill_rating", 0) for player in first_eleven) / 11

        # Calculate strength of substitutes
        substitutes_strength = (
            sum(getattr(player, "skill_rating", 0) for player in substitutes) / len(substitutes)
            if substitutes else 0
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
                (first_eleven_strength * 0.75) +
                (substitutes_strength * 0.25) +
                (age_modifier * 100)
        )

        strength = min(overall_strength / AVG_5_STAR_TRESHOLD * SCALE, 5)
        strength_rounded_to_halves = round(strength * 2) / 2

        return {
            "overall_strength": strength,
            "overall_strength_to_halves": strength_rounded_to_halves,
            "first_eleven_strength": first_eleven_strength,
            "substitutes_strength": substitutes_strength,
            "graphical_club_rating": self._get_graphical_club_rating_repr(strength_rounded_to_halves)
        }

    @staticmethod
    def _get_graphical_club_rating_repr(strength_rounded_to_halves):
        star_symbol = '★'
        half_symbol = '½'
        output = '['
        output += star_symbol * floor(strength_rounded_to_halves)
        output += half_symbol if strength_rounded_to_halves % 1 else ''
        output += ']'
        return output
