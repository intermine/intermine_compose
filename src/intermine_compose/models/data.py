"""Data model."""

from sqlalchemy import Column, String

from intermine_compose.models.meta.mixins import (
    CRUDMixin,
    Model,
    SurrogatePK,
    TimestampMixin,
)


class DataFile(TimestampMixin, Model, SurrogatePK, CRUDMixin):
    """DataFile model."""

    name = Column(String(100), nullable=False)
    fileFormat = Column(String, nullable=False)
    organisms = Column(String(), nullable=False)
    # user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    # user = relationship(
    #     "User", back_populates="data_files", lazy="joined", single_parent=True
    # )
    # mine_id = Column(UUID(as_uuid=True), ForeignKey("mine.id"))
    # mine = relationship("Mine", back_populates="data_files", lazy="joined", single_parent=True)


# class DataFileSchema(Schema):
#     fileId = fields.UUID(required=True)
#     name = fields.String(required=True)
#     # fileFormat = fields.String(required=True)
#     # organisms = fields.String(required=True)


# class DataFileUploadSchema(Schema):
#     mineId = fields.UUID(required=True)


# class DataFileRemoteUploadSchema(Schema):
#     mineId = fields.UUID(required=True)
#     remoteURL = fields.Url(required=True)
