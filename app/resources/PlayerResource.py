from app.database.schemas.PlayerSchema import PlayerSchema
from sqlalchemy.orm import Session

class PlayerResource:
    """Handles operations related to Player entities in the database."""
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_players(self):
        """Retrieve all players from the database."""
        return self.db_session.query(PlayerSchema).all()

    def get_player_by_id(self, player_id: int):
        """Retrieve a single player by their ID."""
        return self.db_session.query(PlayerSchema).filter_by(player_id=player_id).first()

    def create_player(self, player_data: dict):
        """Create a new player in the database."""
        new_player = PlayerSchema(**player_data)
        self.db_session.add(new_player)
        self.db_session.commit()
        return new_player

    def delete_player(self, player_id: int):
        """Delete a player from the database."""
        player = self.get_player_by_id(player_id)
        if player:
            self.db_session.delete(player)
            self.db_session.commit()
        return player