# """Template model."""

# from sqlalchemy import Column, String

# from intermine_compose.models.meta.mixins import (
#     CRUDMixin,
#     Model,
#     SurrogatePK,
#     TimestampMixin,
# )


# class Template(TimestampMixin, Model, SurrogatePK, CRUDMixin):
#     """Template model."""

#     name = Column(String(100), nullable=False)
#     data = Column(String, nullable=False)
