"""Models module for Flask User API."""

from datetime import UTC, datetime

from sqlalchemy.orm import Mapped, mapped_column

from .extensions import db


class User(db.Model):
    """
    User model representing a user in the system.

    Attributes:
        id: The unique identifier for the user
        name: The user's full name (2-128 characters)
        email: The user's email address (unique)
        created_at: Timestamp of when the user was created
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(128), nullable=False)
    email: Mapped[str] = mapped_column(db.String(128), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    def __repr__(self) -> str:
        """
        Return string representation of User for debugging.
        """
        return f"User {self.email}"

    def __str__(self) -> str:
        """
        Return string representation of User for display.
        """
        return f"User name: {self.name} User email: {self.email}"
