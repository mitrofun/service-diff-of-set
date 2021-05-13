import databases
import sqlalchemy
import ormar

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
