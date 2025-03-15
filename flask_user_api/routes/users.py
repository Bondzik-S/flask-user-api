"""Routes module for user-related endpoints."""

from typing import Any

from flask import Blueprint, abort, request
from sqlalchemy.exc import IntegrityError

from flask_user_api.extensions import db
from flask_user_api.models import User
from flask_user_api.schemas import UserSchema

users_bp = Blueprint("users", __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

JsonResponse = dict[str, Any] | list[dict[str, Any]]
RouteResponse = tuple[JsonResponse, int]


@users_bp.route("", methods=["POST"])
def create_user() -> RouteResponse:
    """Create a new user.

    Expects JSON with name and email fields.
    Returns created user data or error message.

    Returns:
        Tuple containing JSON response and HTTP status code.

    Status Codes:
        201: User created successfully
        400: Validation error
        409: Email already exists
        415: Invalid content type
    """
    if not request.is_json:
        return {"error": "Invalid content type"}, 415

    data = request.get_json() or {}

    errors = user_schema.validate(data)
    if errors:
        return errors, 400

    if User.query.filter_by(email=data["email"]).first():
        return {"error": "User with this email already exists"}, 409

    new_user = User(name=data["name"], email=data["email"])

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Database error occurred"}, 400

    return user_schema.dump(new_user), 201


@users_bp.route("", methods=["GET"])
def get_users() -> RouteResponse:
    """Get all users.

    Returns a list of all users in the system.

    Returns:
        Tuple containing JSON response and HTTP status code.

    Status Codes:
        200: Success
    """
    all_users = User.query.all()
    return users_schema.dump(all_users), 200


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int) -> RouteResponse:
    """Get a specific user by ID.

    Args:
        user_id: The ID of the user to retrieve.

    Returns:
        Tuple containing JSON response and HTTP status code.

    Status Codes:
        200: Success
        404: User not found
    """
    user = db.session.get(User, user_id)
    if not user:
        abort(404, description="User not found")
    return user_schema.dump(user), 200


@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id: int) -> RouteResponse:
    """Update a specific user.

    Args:
        user_id: The ID of the user to update.

    Returns:
        Tuple containing JSON response and HTTP status code.

    Status Codes:
        200: Success
        400: Validation error
        404: User not found
        415: Invalid content type
    """
    if not request.is_json:
        return {"error": "Invalid content type"}, 415

    user = db.session.get(User, user_id)
    if not user:
        abort(404, description="User not found")

    data = request.get_json() or {}
    errors = user_schema.validate(data, partial=True)
    if errors:
        return errors, 400

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email already exists"}, 400

    return user_schema.dump(user), 200


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int) -> RouteResponse:
    """Delete a specific user.

    Args:
        user_id: The ID of the user to delete.

    Returns:
        Tuple containing JSON response and HTTP status code.

    Status Codes:
        200: Success
        404: User not found
    """
    user = db.session.get(User, user_id)
    if not user:
        abort(404, description="User not found")

    db.session.delete(user)
    db.session.commit()

    return {"message": "User deleted"}, 200
