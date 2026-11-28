from alembic import context
from wattwise.config import Settings
from wattwise.db import build_engine

config = context.config


def run_migrations():
    # No interpolation of credentials through logging or Alembic ini strings.
    engine = build_engine(Settings().database_url)
    try:
        if context.is_offline_mode():
            context.configure(url=engine.url, literal_binds=True)
            with context.begin_transaction():
                context.run_migrations()
        else:
            with engine.connect() as connection:
                context.configure(connection=connection)
                with context.begin_transaction():
                    context.run_migrations()
    finally:
        engine.dispose()


run_migrations()
