"""User model."""

from datetime import datetime, timedelta
from time import time
from typing import Any, Dict, Union

from flask import current_app
from jose import jwt
# import jwt
from playhouse.postgres_ext import BigBitField, BooleanField, CharField

from intermine_compose.extentions import pwd_context, settings
from intermine_compose.models.meta.mixins import BaseModel


# User class for storing user data in database
class Actor(BaseModel):
    """An actor in the app."""

    __tablename__ = "actor"
    firstName = CharField(max_length=100, null=True)  # Column(String(80))
    lastName = CharField(max_length=100, null=True)  # Column(String(80))
    name = CharField(max_length=200, null=True)  # Column(db.String(100), nullable=True)
    organisation = CharField(max_length=100, null=True)  # Column(String(80))
    email = CharField(
        max_length=200, null=False
    )  # Column(String(120), unique=True, nullable=False)
    # Hashed password
    password = BigBitField(null=True)  # Column(db.LargeBinary(128), nullable=True)
    active = BooleanField(default=False)  # Column(db.Boolean(), default=False)
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
        BaseModel.__init__(self, name=name, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

        if email:
            self.email = email.lower()

    def set_password(self: "Actor", password: str) -> None:
        """Set password."""
        self.password = pwd_context.hash(password)

    def check_password(self: "Actor", value: str) -> bool:
        """Check password."""
        return pwd_context.verify(value, self.password)

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

    @staticmethod
    def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
    ) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def __repr__(self: "Actor") -> str:
        """Represent instance as a unique string."""
        return f"<User({self.email!r})>"
