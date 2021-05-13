import sys
import os

from logging.config import fileConfig
from sqlalchemy import create_engine

from alembic import context

from src.config import settings
from src.models import Calculation

sys.path.append(os.getcwd())
config = context.config

fileConfig(config.config_file_name)

# note how it's 'raw' metadata not the one attached to Base as there is no Base
target_metadata = Calculation.Meta.metadata
URL = settings.db_url


def run_migrations_offline():

    context.configure(
        url=URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        user_module_prefix='sa.'
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            user_module_prefix='sa.'
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
