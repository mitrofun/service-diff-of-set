import os

import sqlalchemy

from src.config import settings

from src.models import Calculation


def pytest_sessionstart(session):
    """Migrations database."""
    engine = sqlalchemy.create_engine(settings.db_url)
    Calculation.Meta.metadata.create_all(engine)


def pytest_sessionfinish(session, exitstatus):
    """Whole test run finishes. """
    filename = settings.db_url.split('///')[-1]
    os.remove(filename)
