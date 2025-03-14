from flask import Flask
from flask_migrate import Migrate

from .config import Config
from .extensions import db, ma

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    migrate = Migrate(app, db)

    # # Реєстрація blueprints (якщо вони є)
    # from .routes import users_bp  # припустимо, ми маємо blueprint у routes/__init__.py
    # app.register_blueprint(users_bp, url_prefix='/users')

    return app
