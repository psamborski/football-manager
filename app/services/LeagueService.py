from app.database import get_db_session, LeagueSchema

from app.models.LeagueModel import LeagueModel
from app.resources.LeagueResource import LeagueResource

from app.models.utils import reformat_league_data_from_db


class LeagueService:
    """
    A service class that handles operations related to leagues.
    Provides methods to interact with the database through resources and return formatted league data.
    """

    @staticmethod
    def get_all_leagues():
        """
        Retrieve all available leagues from the database, sorted in descending order by name.
        The retrieved data is reformatted and represented as a list of LeagueModel objects.

        Returns:
            list[LeagueModel]: A list of league models containing the reformatted league data.
        """
        # Access the database session using the context manager
        with get_db_session() as db_session:
            league_resource = LeagueResource(db_session)

            raw_data = league_resource.get_all_leagues(order_by=LeagueSchema.name.asc())

            return [
                LeagueModel(
                    **reformat_league_data_from_db(League)
                ) for League in raw_data
            ]
