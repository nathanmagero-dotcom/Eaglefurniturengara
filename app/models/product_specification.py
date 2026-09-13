from app.extensions import db


class ProductSpecification(db.Model):
    __tablename__ = "product_specifications"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    name = db.Column(db.String(100), nullable=False)

    value = db.Column(db.String(255), nullable=False)

    display_order = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )

    product = db.relationship(
        "Product",
        back_populates="specifications",
    )

    def __repr__(self):
        return f"<ProductSpecification {self.name}: {self.value}>"