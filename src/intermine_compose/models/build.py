# """Build model."""

# from sqlalchemy import Column, String

# from intermine_compose.models.meta.mixins import (
#     CRUDMixin,
#     Model,
#     SurrogatePK,
#     TimestampMixin,
# )


# class Build(TimestampMixin, Model, SurrogatePK, CRUDMixin):
#     """Build model."""

#     kubernetes_task_id = Column(String(100), unique=True, nullable=False)
#     buildStatus = Column(String(100), nullable=False)
# user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
# user = relationship(
#     "User", back_populates="builds", lazy="joined", single_parent=True
# )
# mineId = Column(UUID(as_uuid=True), ForeignKey("mine.id"))
# mine = relationship(
#     "Mine", back_populates="builds", lazy="joined", single_parent=True
# )


# class BuildStatusSchema(Schema):
#     mineId = fields.String(required=True)
#     buildStatus = fields.String(required=True)
#     errorDetails = fields.String(required=False)


# class BuildTriggerSchema(Schema):
#     mineId = fields.String(required=True)
