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

    sku = db.Column(
    db.String(100),
    unique=True,
    nullable=True,
    index=True,
)

    seo_title = db.Column(
    db.String(255),
    nullable=True,
)

    seo_description = db.Column(
    db.Text,
    nullable=True,
)

    active = db.Column(
    db.Boolean,
    default=True,
    nullable=False,
    server_default="1",
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

    category = db.relationship(
        "Category",
        back_populates="products"
    )

    subcategory = db.relationship(
        "Subcategory",
        back_populates="products"
    )

    gallery = db.relationship(
    "ProductImage",
    back_populates="product",
    cascade="all, delete-orphan",
    order_by="ProductImage.display_order",
)

    specifications = db.relationship(
    "ProductSpecification",
    back_populates="product",
    cascade="all, delete-orphan",
    order_by="ProductSpecification.display_order",
)

    # ========================================================
    # REPRESENTATION
    # ========================================================

    def __repr__(self):
        return f"<Product {self.name}>"