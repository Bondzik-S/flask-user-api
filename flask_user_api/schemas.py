"""Schemas module for Flask User API."""

from marshmallow import Schema, fields, validate

from .models import User


class UserSchema(Schema):
    """Schema for serializing and deserializing User objects.

    Attributes:
        name: User's full name, required, 2-128 characters
        email: User's email address, required, must be valid email format
        id: Read-only field, auto-generated
        created_at: Read-only field, auto-generated
    """

    name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=128),
    )
    email = fields.Email(required=True)
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        """Metadata class for UserSchema."""

        model = User
