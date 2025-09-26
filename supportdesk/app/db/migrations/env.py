import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Import your metadata here ---
# Base.metadata will be used for autogenerate
from supportdesk.app.db.base import Base  

target_metadata = Base.metadata

# Prefer a sync URL for Alembic (easier than async here)
# Add this to infra/.env in step C below.
SYNC_DATABASE_URL = os.getenv(
    "SYNC_DATABASE_URL",
    os.getenv("DATABASE_URL", "").replace("+asyncpg", "")
)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = SYNC_DATABASE_URL
    if not url:
        raise RuntimeError("No SYNC_DATABASE_URL or DATABASE_URL set for Alembic")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = SYNC_DATABASE_URL
    if not url:
        raise RuntimeError("No SYNC_DATABASE_URL or DATABASE_URL set for Alembic")
    connectable: Engine = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
