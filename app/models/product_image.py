from app.extensions import db


class ProductImage(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    image = db.Column(db.String(255), nullable=False)

    alt_text = db.Column(db.String(255), nullable=True)

    display_order = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )

    is_primary = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    product = db.relationship(
        "Product",
        back_populates="gallery",
    )

    def __repr__(self):
        return f"<ProductImage {self.image}>"