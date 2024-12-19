import warnings
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, model_validator

from app.database import get_db_session
from app.models.utils import reformat_country_data_from_db
from app.resources.CountryResource import CountryResource

from config import LOGGER


class CountryModel(BaseModel):
    """
    Represents a country entity in the app.models module, managing essential 
    attributes, validation, and database operations for a country object.

    Attributes:
        country_id (Optional[int]): The unique identifier for the country in the database.
        name (Optional[str]): Full name of the country, restricted to 100 characters.
        players_ids (Optional[list[int]]): List of player IDs associated with the country.
    """
    country_id: Optional[int] = Field(default=None, description="ID of the country in the database")
    name: Optional[str] = Field(default=None, description="Name of the country", max_length=100)
    players_ids: Optional[list[int]] = Field(default=None, description="List of players associated with this country")

    @model_validator(mode="after")
    def validate_input(cls, values):
        """
        Validates the input fields of the `CountryModel`.

        Rules for valid configurations:
        1. Only `country_id` is provided; all other fields are `None`.
        2. All fields except `country_id` are provided and not `None`.
        3. All fields are provided, including `country_id`.

        This ensures logical consistency in country data states.

        Raises:
            ValueError: If the `CountryModel` does not fit any of the allowed configurations.
        """
        entries = {**values.model_dump()}
        del entries["players_ids"]  # exclude players from validation; including them (or not including them) won't affect object integrity

        # Check if there's only country_id
        has_only_country_id = entries.get("country_id", None) is not None and all(
            value is None for key, value in entries.items() if key != "country_id"
        )

        # Check if there are all fields but country_id
        has_all_but_country_id = entries.get("country_id", None) is None and all(
            value is not None for key, value in entries.items() if key != "country_id"
        )

        # Check if there are all fields
        has_all_fields = all(
            value is not None for key, value in entries.items()
        )

        if not (has_only_country_id or has_all_but_country_id or has_all_fields):
            raise ValueError(
                "Invalid country data. You should:\n"
                "1. Pass 'country_id' only.\n"
                "2. Pass all other fields except 'country_id'.\n"
                "3. All fields at once.\n"
                "Possible fields: country_id (int), name (str) players_ids (list[int]) [always optional]."
            )
        return values

    def fetch_data_by_id(self) -> "CountryModel":
        """
        Fetches a country's details using the `country_id` key.

        Retrieves data from the database, reformats it, and updates the 
        current `CountryModel` instance with valid values.

        Raises:
            ValueError: If no country record is found for the given `country_id`.
            ValidationError: If the fetched data does not pass validation.
        """
        with get_db_session() as db_session:
            country_resource = CountryResource(db_session)
            country = country_resource.get_country_by_id(self.country_id)

            if not country:
                raise ValueError(f"Country with ID {self.country_id} does not exist.")

            country_data = reformat_country_data_from_db(country)

            if self.model_validate(country_data):
                self.__dict__.update(country_data)
                return self
            else:
                raise ValidationError("Country data is invalid.")

    def create_country(self):
        """
        Creates a new country entry in the database using this instance's data 
        and assigns newly generated data to the current instance.

        Notes:
            - `country_id` is auto-generated by the database when creating a new country.
            - This method doesn't update players' country affiliations; it must be done manually.

        Raises:
            ValueError: If required fields for country creation are incomplete.
            ValidationError: If the database-generated country data fails validation.
        """

        country_data = self.model_dump(exclude={"country_id", "players_ids"})

        LOGGER.warning("Country ID will be generated automatically in the database.")
        LOGGER.warning("Creating a country won't update players' country affiliations. Please update them manually.")
        print(warnings.warn("Country ID will be generated automatically in the database."))
        print(warnings.warn("Creating a country won't update players' country affiliations. Please update them manually."))

        with get_db_session() as db_session:
            country_resource = CountryResource(db_session)
            try:
                new_country = country_resource.create_country(country_data)
            except Exception as e:
                raise ValueError("Failed to create country.")

            if new_country:
                country_data = reformat_country_data_from_db(new_country)
                if self.model_validate(country_data):
                    self.__dict__.update(country_data)
                    return self
                else:
                    raise ValidationError("Country data is invalid.")
            else:
                raise ValueError("Failed to create country.")

    def __str__(self):
        """
        Returns a string representation of the country's information, 
        showcasing key attributes in a readable format.
        """
        return (
            f"COUNTRY ID {self.country_id}\n"
            f"Name: {self.name}\n"
            f"Players' IDs (showing max. 20): {self.players_ids[:20] or '-'}\n"
        )
