import logging

from flask import Flask

from app.routes import bp
from config import BASE_DIR


def create_app() -> Flask:
    logging.basicConfig(level=logging.INFO)

    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    app.register_blueprint(bp)
    return app
