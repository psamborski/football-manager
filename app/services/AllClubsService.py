from app.database import get_db_session, ClubSchema
from app.models.ClubModel import ClubModel
from app.models.utils import reformat_club_data_from_db
from app.resources.ClubResource import ClubResource


class AllClubsService:
    """
    AllClubsService provides functionality to fetch and process club-related data.
    Created for operating on multiple clubs data.
    """

    @staticmethod
    def get_clubs_by_league_id(league_id):
        """
        Fetch and process the clubs from a specific league.

        Args:
            league_id (int): The ID of the league for which clubs will be fetched.

        Returns:
            List[ClubModel]: A list of ClubModel objects representing the top clubs
            from the specified league, ordered alphabetically by name.
        """
        with get_db_session() as db_session:
            club_resource = ClubResource(db_session)

            raw_clubs = club_resource.get_clubs_by_league_id(
                league_id, order_by=ClubSchema.name.asc()
            )

            return [
                ClubModel(
                    **reformat_club_data_from_db(club)
                ) for club in raw_clubs
            ]
