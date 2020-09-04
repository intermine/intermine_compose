"""User model."""

from datetime import datetime, timedelta
from typing import Union

from jose import jwt, JWTError
from playhouse.postgres_ext import BooleanField, CharField

from intermine_compose.extentions import pwd_context, settings
from intermine_compose.models.meta.mixins import BaseModel


# User class for storing user data in database
class Actor(BaseModel):
    """An actor in the app."""

    name = CharField(max_length=200, null=True)
    organisation = CharField(max_length=100, null=True)
    email = CharField(max_length=200, null=False)
    # Hashed password
    password = CharField(null=True)
    active = BooleanField(default=False)
    # mines = relationship("Mine", back_populates="user", lazy="joined")
    # data_files = relationship("DataFile", back_populates="user", lazy="joined")
    # builds = relationship("Build", back_populates="user", lazy="joined")
    # active_mine_quota = Column(Integer, default=1)
    # inactive_mine_quota = Column(Integer, default=5)
    # daily_mine_build_quota = Column(Integer, default=5)
    # storage_quota = Column(Integer, default=500)

    def set_password(self: "Actor", password: str) -> None:
        """Set password."""
        self.password = pwd_context.hash(password)

    def check_password(self: "Actor", plain_password: str) -> bool:
        """Check password."""
        return pwd_context.verify(plain_password, self.password)

    def create_reset_password_token(
        self: "Actor", expires_delta: timedelta = None
    ) -> str:
        """Create password reset token for user."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": f"email:{self.email}", "reset_token": "1"}
        encoded_jwt = jwt.encode(
            to_encode, settings.APP_SECRET, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def verify_reset_password_token(token: Union[str, bytes]) -> Union[None, "Actor"]:
        """Verify reset tokens."""
        try:
            payload = jwt.decode(
                token, settings.APP_SECRET, algorithms=[settings.ALGORITHM]
            )
            if int(payload.get("reset_token")) != 1:
                return None
            email: str = payload.get("sub").split(":")[1]
            if email is None:
                return None
        except JWTError:
            raise JWTError

        user_list = Actor.select().where(Actor.email == email)
        if len(user_list) != 1:
            return None
        return user_list[0]

    def create_access_token(self: "Actor", expires_delta: timedelta = None) -> str:
        """Create access token for user."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": f"email:{self.email}"}
        encoded_jwt = jwt.encode(
            to_encode, settings.APP_SECRET, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def verify_access_token(token: Union[str, bytes]) -> Union[None, "Actor"]:
        """Verify access tokens."""
        token = token.split(" ")[1]
        try:
            payload = jwt.decode(
                token, settings.APP_SECRET, algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("sub").split(":")[1]
            if email is None:
                return None
        except JWTError:
            raise JWTError

        user_list = Actor.select().where(Actor.email == email)
        if len(user_list) != 1:
            return None
        return user_list[0]

    def __repr__(self: "Actor") -> str:
        """Represent instance as a unique string."""
        return f"<User({self.email!r})>"
