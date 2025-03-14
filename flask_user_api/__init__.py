from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from .config import Config
from .extensions import db, ma

def create_app(config_class=Config):
    app = Flask(__name__, static_folder="../static")
    app.config["DEBUG"]=True
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)

    CORS(app)

    from .routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    SWAGGER_URL = "/docs"
    API_URL = "/static/swagger.json"
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            "app_name": "Flask User API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
