"""App database."""

from contextvars import ContextVar
from typing import Any

from fastapi import Depends
from logzero import logger
import peewee
from playhouse.postgres_ext import PostgresqlExtDatabase
from pydantic.utils import GetterDict

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
        autorollback=True,
    )


# hacks to make peewee work with FastAPI
db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    """Modified peewee connection state."""

    def __init__(self: "PeeweeConnectionState", **kwargs) -> None:
        """Initialize class."""
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self: "PeeweeConnectionState", name: Any, value: Any) -> None:
        """Add attr."""
        self._state.get()[name] = value

    def __getattr__(self: "PeeweeConnectionState", name: Any) -> Any:
        """Get attr."""
        return self._state.get()[name]


class PeeweeGetterDict(GetterDict):
    """Convert pewee model instances to pydantic."""

    def get(self: "PeeweeGetterDict", key: Any, default: Any = None):
        """Get dict."""
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


# create a db object shared by entire app
db = create_db(settings)
db._state = PeeweeConnectionState()


async def reset_db_state() -> None:
    """Reset DB state."""
    db._state._state.set(db_state_default.copy())
    db._state.reset()


def get_db(db_state: Any = Depends(reset_db_state)) -> Any:  # noqa
    """Provides db connection to route handlers."""
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()


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
        db.commit()
    except BaseException as e:
        logger.error(f"Failed to reset tables\n\n Error Message: {e} \n\n")
    db.close()


def reset_test_db(db: PostgresqlExtDatabase) -> None:
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
        db.commit()
    except BaseException as e:
        logger.error(f"Failed to reset tables\n\n Error Message: {e} \n\n")


def destroy_test_db(db: PostgresqlExtDatabase) -> None:
    """Destroy database."""
    # Drop tables
    try:
        db.drop_tables(tables_list)
    except BaseException as e:
        logger.error(f"Failed to drop tables\n\n Error Message: {e} \n\n")
    db.close()
