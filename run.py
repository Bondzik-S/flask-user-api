"""Entry point for Flask User API."""

from flask_user_api import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
