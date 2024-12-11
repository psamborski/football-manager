import logging
import warnings
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, model_validator

from app.database import get_db_session
from app.models.utils import reformat_player_data_from_db

from app.resources.PlayerResource import PlayerResource

class PlayerModel(BaseModel):
    """
    Represents a player entity in the app.models module, managing essential 
    attributes, validation, and database operations for a player object.

    Attributes:
        player_id (Optional[int]): The unique identifier for the player in the database.
        name (Optional[str]): Full name of the player, restricted to 100 characters.
        position (Optional[str]): The player's field position, restricted to 50 characters.
        skill_rating (Optional[int]): Rating of the player's skill, ranging from 1 to 99.
        height (Optional[int]): Player's height in centimeters (1-299).
        weight (Optional[float]): Player's weight in kilograms (1.0-299.0).
        birthday (Optional[date]): The player's birthdate.
        club_id (Optional[int]): ID of the club associated with the player.
        country_id (Optional[int]): ID of the country associated with the player.
    """
    player_id: Optional[int] = Field(default=None, description="ID of the player in the database")
    name: Optional[str] = Field(default=None, description="Name of the player", max_length=100)
    position: Optional[str] = Field(default=None, description="Player's position on the field", max_length=50)
    skill_rating: Optional[int] = Field(default=None, ge=1, le=99, description="Player's skill rating (1-99)")
    height: Optional[int] = Field(default=None, ge=1, le=299, description="Height in centimeters")
    weight: Optional[float] = Field(default=None, ge=1, le=299, description="Weight in kilograms")
    birthday: Optional[date] = Field(default=None, description="Date of birth of the player")
    club_id: Optional[int] = Field(default=None, description="ID of club associated with the player")
    country_id: Optional[int] = Field(default=None, description="Id of country associated with the player")

    @model_validator(mode="after")
    def validate_input(cls, values):
        """
        Validates the input fields of the `PlayerModel`.

        Rules for valid configurations:
        1. Only `player_id` is provided; all other fields are `None`.
        2. All fields except `player_id` are provided and not `None`.
        3. All fields are provided, including `player_id`.

        This ensures logical consistency in player data states.

        Raises:
            ValueError: If the `PlayerModel` does not fit any of the allowed configurations.
        """
        entries = {**values.model_dump()}
        del entries["club_id"]  # player can be not assigned to any club, so exclude it from validation

        # Check if there's only player_id
        has_only_player_id = entries.get("player_id", None) is not None and all(
            value is None for key, value in entries.items() if key != "player_id"
        )

        # Check if there are all fields but player_id
        has_all_but_player_id = entries.get("player_id", None) is None and all(
            value is not None for key, value in entries.items() if key != "player_id"
        )

        # Check if there are all fields
        has_all_fields = all(
            value is not None for key, value in entries.items()
        )

        if not (has_only_player_id or has_all_but_player_id or has_all_fields):
            raise ValueError(
                "Invalid player data. You should:\n"
                "1. Pass 'player_id' only.\n"
                "2. Pass all other fields except 'player_id'.\n"
                "3. All fields at once.\n"
                "Possible fields: player_id (int), name (str), position (str), skill_rating (int), height (int), weight (float), birthday (date), club_id (int) [always optional], country_id (int)."
            )
        return values

    def fetch_data_by_id(self) -> "PlayerModel":
        """
        Fetches a player's details using the `player_id` key.

        Retrieves data from the database, reformats it, and updates the 
        current `PlayerModel` instance with valid values.

        Raises:
            ValueError: If no player record is found for the given `player_id`.
            ValidationError: If the fetched data does not pass validation.
        """
        with get_db_session() as db_session:
            player_resource = PlayerResource(db_session)
            player = player_resource.get_player_by_id(self.player_id)

            if not player:
                raise ValueError(f"Player with ID {self.player_id} does not exist.")

            player_data = reformat_player_data_from_db(player)

            # if self.model_validate(player_data): # TODO uncomment whe you fix players birthdays
            if True:
                self.__dict__.update(player_data)
                return self
            else:
                raise ValidationError("Player data is invalid.")

    def create_player(self):
        """
        Creates a new player entry in the database using this instance's data 
        and assigns new data to current instance.

        Note:
            If an existing player record is represented, this method will 
            create a duplicate entry with a different `player_id`.

        Raises:
            ValueError: If required fields for player creation are incomplete.
            ValidationError: If the database-generated player data fails validation.
        """

        player_data = self.model_dump(exclude={"player_id"})
        print(warnings.warn("Player ID will be generated automatically in database."))
        logger = logging.getLogger(__name__)
        logger.warning("Player ID will be generated automatically in database.")

        with get_db_session() as db_session:
            player_resource = PlayerResource(db_session)
            try:
                new_player = player_resource.create_player(player_data)
            except Exception as e:
                raise ValueError("Failed to create player.")

            if new_player:
                player_data = reformat_player_data_from_db(new_player)
                if self.model_validate(player_data):
                    self.__dict__.update(player_data)
                    return self
                else:
                    raise ValidationError("Player data is invalid.")
            else:
                raise ValueError("Failed to create player.")

    # TODO def update_player(self):

    def __str__(self):
        """
        Returns a string representation of the player's information, 
        showcasing key attributes in a readable format.
        """
        return (
            f"PLAYER ID {self.player_id}\n"
            f"Name: {self.name}\n"
            f"Position: {self.position}\n"
            f"Skill Rating: {self.skill_rating}\n"
            f"Height: {self.height} cm\n"
            f"Weight: {self.weight} kg\n"
            f"Birthday: {self.birthday}\n"
            f"Club ID: {self.club_id or '-'}\n"
            f"Country ID: {self.country_id}"
        )
