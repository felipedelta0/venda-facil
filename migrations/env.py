import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Configuração Alembic
config = context.config

# Carrega o log configurado em alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Aqui você pode importar seus modelos
# from yourapp import models
# target_metadata = models.Base.metadata
target_metadata = None  # se não tiver metadata, mantenha None

# Pega a URL do banco do ambiente
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise Exception("DATABASE_URL não definida no ambiente.")

config.set_main_option("sqlalchemy.url", database_url)


def run_migrations_offline():
    """Executa migrações no modo 'offline'."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Executa migrações no modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
