"""Helper ORM functions."""

from typing import Dict

from playhouse.postgres_ext import ForeignKeyField


def reference_col(
    tablename: str,
    nullable: bool = False,
    pk_name: str = "id",
    foreign_key_kwargs: Dict = None,
    column_kwargs: Dict = None,
) -> ForeignKeyField:
    """Column that adds primary key foreign key reference.

    Args:
        tablename (str): name of the table.
        nullable (bool): is nullable?
        pk_name (str): name of the primary key field.
        foreign_key_kwargs (Dict): Dict of args for fk.
        column_kwargs (Dict): Dict of args for column.

    Returns:
        Return the Column.

    Examples: ::
        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return ForeignKeyField(
        f"{tablename}.{pk_name}", null=nullable, **foreign_key_kwargs
    )
