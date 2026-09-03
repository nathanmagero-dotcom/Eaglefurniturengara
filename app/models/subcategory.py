from app.extensions import db


class Subcategory(db.Model):

    __tablename__ = "subcategories"

    # ==========================================================
    # PRIMARY KEY
    # ==========================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================================================
    # CATEGORY
    # ==========================================================

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False,
        index=True
    )

    # ==========================================================
    # BASIC INFORMATION
    # ==========================================================

    name = db.Column(
        db.String(100),
        nullable=False
    )

    slug = db.Column(
        db.String(120),
        nullable=False,
        unique=True,
        index=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    # ==========================================================
    # VISUAL INFORMATION
    # ==========================================================

    icon = db.Column(
        db.String(100),
        nullable=True
    )

    image = db.Column(
        db.String(255),
        nullable=True
    )

    # ==========================================================
    # STOREFRONT SETTINGS
    # ==========================================================

    active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    display_order = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    # ==========================================================
    # RELATIONSHIPS
    # ==========================================================

    category = db.relationship(
        "Category",
        back_populates="subcategories"
    )

    products = db.relationship(
        "Product",
        back_populates="subcategory",
        lazy=True
    )

    # ==========================================================
    # REPRESENTATION
    # ==========================================================

    def __repr__(self):
        return f"<Subcategory {self.name}>"