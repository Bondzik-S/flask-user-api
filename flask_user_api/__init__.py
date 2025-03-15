"""Flask User API application package."""

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

from .config import Config
from .extensions import db, ma


def create_app(config_class: type[Config] = Config) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_class: Configuration class to use (default: Config).

    Returns:
        Configured Flask application instance.

    The function initializes the Flask application with:
        - Database connection
        - Marshmallow for serialization
        - Database migrations
        - CORS support
        - API routes
        - Swagger UI documentation
    """
    app = Flask(__name__, static_folder="../static")
    app.config["DEBUG"] = True
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)

    CORS(app)

    from .routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    SWAGGER_URL = "/docs"
    API_URL = "/static/swagger.json"
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            "app_name": "Flask User API",
        },
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
