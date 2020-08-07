# """Mine model."""

# from sqlalchemy import Column, String

# from intermine_compose.models.meta.mixins import (
#     CRUDMixin,
#     Model,
#     SurrogatePK,
#     TimestampMixin,
# )


# class Mine(TimestampMixin, Model, SurrogatePK, CRUDMixin):
#     """Mine model."""

#     mineName = Column(String(), unique=True, nullable=False)
#     minelocation = Column(String(100), unique=True, nullable=False)
#     mineStatus = Column(String(), nullable=False)
#     privacy = Column(String(), nullable=False)
#     license = Column(String(), nullable=False)
#     config = Column(String(), nullable=False)
#     templates = Column(String(), nullable=True)
# user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
# user = relationship(
#     "User", back_populates="mines", lazy="joined", single_parent=True
# )
# data_files = relationship("DataFile", back_populates="mine", lazy="joined")
# builds = relationship("Build", back_populates="mine", lazy="joined")


# class MineSchema(ma.Schema):
#     mineName = fields.String(required=True)
#     minelocation = fields.Url(required=True)
#     mineStatus = fields.String(required=True)
#     privacy = fields.String(required=True)


# class MineStateSchema(ma.Schema):
#     mineStatus = fields.String(required=True)


# class MineCheckNameSchema(ma.Schema):
#     mineName = fields.String(required=True)
#     isAvailable = fields.String(required=False)
