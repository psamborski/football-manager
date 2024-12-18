from app.database import get_db_session, CountrySchema

from app.models.CountryModel import CountryModel
from app.resources.CountryResource import CountryResource

from app.utils import reformat_country_data_from_db


class CountryService:
    @staticmethod
    def get_all_countries():
        with get_db_session() as db_session:
            country_resource = CountryResource(db_session)
            raw_data = country_resource.get_all_countries(order_by=CountrySchema.name.desc())

            return [
                CountryModel(
                    **reformat_country_data_from_db(country)
                ) for country in raw_data
            ]
