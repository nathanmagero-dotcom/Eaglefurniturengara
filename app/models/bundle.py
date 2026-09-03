from app.extensions import db


class Bundle(db.Model):

    __tablename__ = "bundles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    slug = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    description = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(255)
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    sale_price = db.Column(
        db.Float
    )

    featured = db.Column(
        db.Boolean,
        default=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    items = db.relationship(
        "BundleItem",
        back_populates="bundle",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Bundle {self.name}>"