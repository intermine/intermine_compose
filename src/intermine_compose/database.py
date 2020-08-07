"""App database."""

from logzero import logger
from playhouse.postgres_ext import PostgresqlExtDatabase

from intermine_compose.config import DefaultConfig
from intermine_compose.extentions import settings


def create_db(config: DefaultConfig) -> PostgresqlExtDatabase:
    """Create database."""
    return PostgresqlExtDatabase(
        config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASS,
        host=config.DB_HOST,
        port=config.DB_PORT,
        autorollback=False,
        autocommit=False,
    )


# create a db object shared by entire app
db = create_db(settings)


# hack for now to workaround circular import
from intermine_compose.models import Actor  # noqa

tables_list = [Actor]


def init_db(db: PostgresqlExtDatabase) -> None:
    """Initialize database."""
    # Open a database connection
    try:
        db.connect()
    except BaseException as e:
        logger.error(
            f"Failed to create connection to database!!!\n\n Error Message: {e} \n\n"
        )

    # Create tables
    try:
        db.create_tables(tables_list)
        db.commit()
    except BaseException as e:
        logger.error(f"Failed to create tables\n\n Error Message: {e} \n\n")
    db.close()


def destroy_db(db: PostgresqlExtDatabase) -> None:
    """Destroy database."""
    # Open a database connection
    try:
        db.connect()
    except BaseException as e:
        logger.error(
            f"Failed to create connection to database!!!\n\n Error Message: {e} \n\n"
        )

    # Create tables
    try:
        db.drop_tables(tables_list)
    except BaseException as e:
        logger.error(f"Failed to drop tables\n\n Error Message: {e} \n\n")
    db.close()


def reset_db(db: PostgresqlExtDatabase) -> None:
    """Initialize database."""
    # Open a database connection
    try:
        db.connect()
    except BaseException as e:
        logger.error(
            f"Failed to create connection to database!!!\n\n Error Message: {e} \n\n"
        )

    # First Drop tables and then Create tables
    try:
        db.drop_tables(tables_list)
        db.create_tables(tables_list)
    except BaseException as e:
        logger.error(f"Failed to reset tables\n\n Error Message: {e} \n\n")
    db.close()

