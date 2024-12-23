# Redundant loading (database/__init__.py) but imports are easier (I can use simply from database.schemas import PlayerSchema)
from .ClubSchema import ClubSchema
from .CountrySchema import CountrySchema
from .LeagueSchema import LeagueSchema
from .PlayerSchema import PlayerSchema