from app.extensions import db
from datetime import datetime


class Website(db.Model):
    __tablename__ = "website"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    company_name = db.Column(
        db.String(150),
        nullable=False,
        default="Eagle Furniture Ngara"
    )

    tagline = db.Column(
        db.String(255),
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    phone = db.Column(
        db.String(50),
        nullable=True
    )

    email = db.Column(
        db.String(120),
        nullable=True
    )

    location = db.Column(
        db.String(255),
        nullable=True
    )

    logo = db.Column(
        db.String(255),
        nullable=True
    )

    hero_title = db.Column(
        db.String(255),
        nullable=True
    )

    hero_description = db.Column(
        db.Text,
        nullable=True
    )

    facebook = db.Column(
        db.String(255),
        nullable=True
    )

    instagram = db.Column(
        db.String(255),
        nullable=True
    )

    youtube = db.Column(
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
        return f"<Website {self.company_name}>"