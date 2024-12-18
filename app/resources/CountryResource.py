from sqlalchemy.orm import Session

from app.database.schemas.CountrySchema import CountrySchema
from app.resources.utils import validate_order_by_param, validate_limit_param


class CountryResource:
    """This resource class provides methods to interact with Country entities in the database.

    Methods:
        - get_all_countries: Retrieve a list of all countries, with optional filters for limit and order.
        - get_country_by_id: Retrieve a specific country identified by its unique ID.
        - create_country: Add a new country entry to the database.
        - delete_country: Remove an existing country from the database.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_countries(self, limit=None, order_by=None):
        """Retrieve all countries from the database.

        Args:
            limit (int, optional): The maximum number of countries to retrieve.
            order_by (str, optional): The field to order the results by.

        Returns:
            List[CountrySchema]: A list of CountrySchema objects representing the countries.
        """
        query = self.db_session.query(CountrySchema)

        if validate_order_by_param(order_by):
            query = query.order_by(order_by)
        if validate_limit_param(limit):
            query = query.limit(limit)

        return query.all()

    def get_country_by_id(self, country_id: int):
        """Retrieve a single country by its unique ID.

        Args:
            country_id (int): The unique identifier of the country.

        Returns:
            CountrySchema or None: The country object if found, otherwise None.
        """
        return self.db_session.query(CountrySchema).filter_by(country_id=country_id).first()

    def create_country(self, country_data: dict):
        """Create a new country in the database.

        Args:
            country_data (dict): A dictionary containing the details of the country to be created.
                Example: {"name": "Canada", "code": "CA"}

        Returns:
            CountrySchema: The newly created country object.
        """
        new_country = CountrySchema(**country_data)
        self.db_session.add(new_country)
        self.db_session.commit()
        return new_country

    def delete_country(self, country_id: int):
        """Delete a country from the database using its unique ID.

        Args:
            country_id (int): The unique identifier of the country to delete.

        Returns:
            CountrySchema or None: The deleted country object if it existed, otherwise None.
        """
        country = self.get_country_by_id(country_id)
        if country:
            self.db_session.delete(country)
            self.db_session.commit()
        return country
