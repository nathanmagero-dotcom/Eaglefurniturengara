from app.extensions import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = "products"

    # ========================================================
    # PRIMARY KEY
    # ========================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ========================================================
    # BASIC PRODUCT INFORMATION
    # ========================================================

    name = db.Column(
        db.String(150),
        nullable=False
    )

    slug = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    # ========================================================
    # PRICING
    # ========================================================

    price = db.Column(
        db.Float,
        nullable=True
    )

    sale_price = db.Column(
        db.Float,
        nullable=True
    )

    # ========================================================
    # PRODUCT IMAGE
    # ========================================================

    image = db.Column(
        db.String(255),
        nullable=True
    )

    # ========================================================
    # STOREFRONT FLAGS
    # ========================================================

    featured = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    best_seller = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    new_arrival = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    # ========================================================
    # SERVICE
    # ========================================================

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("services.id"),
        nullable=False
    )

    # ========================================================
    # CATEGORY
    # ========================================================

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=True
    )

        # ========================================================
    # SUBCATEGORY
    # ========================================================

    subcategory_id = db.Column(
        db.Integer,
        db.ForeignKey("subcategories.id"),
        nullable=True,
        index=True
    )

    # ========================================================
    # TIMESTAMPS
    # ========================================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ========================================================
    # RELATIONSHIPS
    # ========================================================

    service = db.relationship(
        "Service",
        backref="products"
    )

    category = db.relationship(
        "Category",
        back_populates="products"
    )

    subcategory = db.relationship(
        "Subcategory",
        back_populates="products"
    )

    # ========================================================
    # REPRESENTATION
    # ========================================================

    def __repr__(self):
        return f"<Product {self.name}>"