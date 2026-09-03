from flask import Flask
from dotenv import load_dotenv

from config import Config
from app.extensions import db, migrate

load_dotenv()


def create_app():
    """
    Application factory for Eagle Furniture Ngara.
    """

    app = Flask(__name__)

    app.config.from_object(Config)

    # ---------------------------------------------------------
    # INITIALIZE DATABASE
    # ---------------------------------------------------------

    db.init_app(app)

    # ---------------------------------------------------------
    # INITIALIZE MIGRATIONS
    # ---------------------------------------------------------

    migrate.init_app(app, db)

    # ---------------------------------------------------------
    # LOAD DATABASE MODELS
    # ---------------------------------------------------------

    from app.models import (
        Category,
        Product,
        Bundle,
        BundleItem,
        Website,
        Service,
        Order,
        OrderItem,
    )

    # ---------------------------------------------------------
    # REGISTER MAIN BLUEPRINT
    # ---------------------------------------------------------

    from app.routes import main

    app.register_blueprint(main)

    # ---------------------------------------------------------
    # GLOBAL CART CONTEXT
    # ---------------------------------------------------------

    from app.cart import get_cart_count

    @app.context_processor
    def inject_cart_count():
        return {
            "cart_count": get_cart_count()
        }

    # ---------------------------------------------------------
    # GLOBAL CONFIG CONTEXT
    # ---------------------------------------------------------

    @app.context_processor
    def inject_config():
        return {
            "config": app.config
        }

    # ---------------------------------------------------------
    # RETURN APPLICATION
    # ---------------------------------------------------------

    return app