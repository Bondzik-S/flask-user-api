from flask import Blueprint, request, jsonify, abort

from flask_user_api.models import User
from flask_user_api.extensions import db
from flask_user_api.schemas import UserSchema


users_bp = Blueprint("users", __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_bp.route("", methods=["POST"])
def create_user():
    if not request.is_json:
        return jsonify({"error": "Invalid content type"}), 415

    data = request.get_json() or {}

    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_user = User(name=data["name"], email=data["email"])

    db.session.add(new_user)
    db.session.flush()

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 400
    # return user_schema.jsonify(new_user), 201
    return jsonify(user_schema.dump(new_user)), 201


@users_bp.route("", methods=["GET"])
def get_users():
    all_users = User.query.all()
    return users_schema.jsonify(all_users), 200


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = User.query.get_or_404(user_id, description="User not found")

    return user_schema.jsonify(user), 200


@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if not request.is_json:
        return jsonify({"error": "Invalid content type"}), 415

    user = User.query.get_or_404(user_id, description="User not found")

    data = request.get_json() or {}

    errors = user_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    # if "name" in data:
    #     user.name = data["name"]
    # if "email" in data:
    #     user.email = data["email"]
    try:
        User.query.filter_by(id=user_id).update(data)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 400

    return user_schema.jsonify(user), 200


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id, description="User not found")

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200
