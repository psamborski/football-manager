from app.database import get_db_session, CountrySchema

from app.models.CountryModel import CountryModel
from app.resources.CountryResource import CountryResource

from app.models.utils import reformat_country_data_from_db


class CountryService:
    """
    A service class that handles operations related to countries.
    Provides methods to interact with the database through resources and return formatted country data.
    """

    @staticmethod
    def get_all_countries():
        """
        Retrieve all available countries from the database, sorted in descending order by name.
        The retrieved data is reformatted and represented as a list of CountryModel objects.

        Returns:
            list[CountryModel]: A list of country models containing the reformatted country data.
        """
        # Access the database session using the context manager
        with get_db_session() as db_session:
            country_resource = CountryResource(db_session)

            raw_data = country_resource.get_all_countries(order_by=CountrySchema.name.desc())

            return [
                CountryModel(
                    **reformat_country_data_from_db(country)
                ) for country in raw_data
            ]
