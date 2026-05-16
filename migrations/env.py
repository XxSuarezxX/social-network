import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

import sys
from pathlib import Path

# 1. Agregamos la raíz y la carpeta app_backend al path de Python
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))
sys.path.append(str(root_path / "app_backend"))

# 2. Ahora las importaciones deberían funcionar sin el prefijo app_backend
# (Usa el mismo estilo que tengas en tus archivos de la app)
from core.config import settings
from core.database import Base
from models.user import User  # Asegúrate de importar todos tus modelos aquí
from models.posts import Posts

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations(config_dict: dict) -> None: # Recibe el diccionario corregido
    connectable = async_engine_from_config(
        config_dict, # Usa el diccionario que pasamos
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # 1. Obtenemos la sección del archivo .ini
    configuration = config.get_section(config.config_ini_section, {})
    
    # 2. Inyectamos la URL real desde tu archivo de configuración
    configuration["sqlalchemy.url"] = settings.database_url

    # 3. Se lo pasamos a la función asíncrona
    asyncio.run(run_async_migrations(configuration))


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
