"""User model."""

from time import time
from typing import Dict, Union

from flask import current_app
from flask_login import UserMixin
import jwt
from sqlalchemy import Column, String

from intermine_compose.extentions import bcrypt, db
from intermine_compose.models.meta.mixins import (
    CRUDMixin,
    Model,
    SurrogatePK,
    TimestampMixin,
)


# User class for storing user data in database
class Actor(TimestampMixin, UserMixin, SurrogatePK, Model, CRUDMixin):
    """An actor in the app."""

    __tablename__ = "actor"
    firstName = Column(String(80))
    lastName = Column(String(80))
    name = Column(db.String(100), nullable=True)
    organisation = Column(String(80))
    email = Column(String(120), unique=True, nullable=False)
    # Hashed password
    password = Column(db.LargeBinary(128), nullable=True)
    active = Column(db.Boolean(), default=False)
    # mines = relationship("Mine", back_populates="user", lazy="joined")
    # data_files = relationship("DataFile", back_populates="user", lazy="joined")
    # builds = relationship("Build", back_populates="user", lazy="joined")
    # active_mine_quota = Column(Integer, default=1)
    # inactive_mine_quota = Column(Integer, default=5)
    # daily_mine_build_quota = Column(Integer, default=5)
    # storage_quota = Column(Integer, default=500)

    def __init__(
        self: "Actor", name: str, email: str, password: str = None, **kwargs: Dict
    ) -> None:
        """Create instance."""
        db.Model.__init__(self, name=name, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

        if email:
            self.email = email.lower()

    def set_password(self: "Actor", password: str) -> None:
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self: "Actor", value: str) -> bool:
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def get_reset_password_token(
        self: "Actor", expires_in: int = 600
    ) -> Union[str, bytes]:
        """Get reset password token."""
        return jwt.encode(
            {"reset_password": str(self.id), "exp": time() + expires_in},
            str(current_app.config.get("SECRET_KEY")),
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token: Union[str, bytes]) -> Union[None, "Actor"]:
        """Verify reset token."""
        try:
            id = jwt.decode(
                token, str(current_app.config.get("SECRET_KEY")), algorithms=["HS256"]
            )["reset_password"]
        except BaseException:
            return None
        return Actor.query.filter_by(id=id).first()

    def __repr__(self: "Actor") -> str:
        """Represent instance as a unique string."""
        return f"<User({self.email!r})>"
