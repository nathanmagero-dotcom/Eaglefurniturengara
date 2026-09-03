from app.extensions import db


class Category(db.Model):

    __tablename__ = "categories"

    # ==========================================================
    # PRIMARY KEY
    # ==========================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================================================
    # BASIC INFORMATION
    # ==========================================================

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    slug = db.Column(
        db.String(120),
        nullable=False,
        unique=True,
        index=True
    )

    description = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(255)
    )

    # ==========================================================
    # STOREFRONT SETTINGS
    # ==========================================================

    active = db.Column(
        db.Boolean,
        default=True
    )

    display_order = db.Column(
        db.Integer,
        default=0
    )

    # ==========================================================
    # PRODUCTS
    # ==========================================================

    products = db.relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy=True
    )

    # ==========================================================
    # SUBCATEGORIES
    # ==========================================================

    subcategories = db.relationship(
        "Subcategory",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy=True,
        order_by="Subcategory.display_order"
    )

    # ==========================================================
    # REPRESENTATION
    # ==========================================================

    def __repr__(self):
        return f"<Category {self.name}>"