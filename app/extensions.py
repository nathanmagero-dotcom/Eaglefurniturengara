from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ==========================================================
# DATABASE
# ==========================================================

db = SQLAlchemy()

# ==========================================================
# DATABASE MIGRATIONS
# ==========================================================

migrate = Migrate()