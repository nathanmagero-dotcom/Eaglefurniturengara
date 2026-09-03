from app.extensions import db
from datetime import datetime


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    slug = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    image = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    def __repr__(self):
        return f"<Service {self.name}>"