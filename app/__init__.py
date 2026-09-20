import logging

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.routes import register_routes
from app.visits import init_db
from config import BASE_DIR


def create_app() -> Flask:
    logging.basicConfig(level=logging.INFO)

    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    register_routes(app)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

    init_db()

    return app
