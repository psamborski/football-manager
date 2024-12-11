from app.database.schemas.CountrySchema import CountrySchema
from sqlalchemy.orm import Session

class CountryResource:
    """Handles operations related to Country entities in the database."""
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_countrys(self):
        """Retrieve all countries from the database."""
        return self.db_session.query(CountrySchema).all()

    def get_country_by_id(self, country_id: int):
        """Retrieve a single country by their ID."""
        return self.db_session.query(CountrySchema).filter_by(country_id=country_id).first()

    def create_country(self, country_data: dict):
        """Create a new country in the database."""
        new_country = CountrySchema(**country_data)
        self.db_session.add(new_country)
        self.db_session.commit()
        return new_country

    def delete_country(self, country_id: int):
        """Delete a country from the database."""
        country = self.get_country_by_id(country_id)
        if country:
            self.db_session.delete(country)
            self.db_session.commit()
        return country