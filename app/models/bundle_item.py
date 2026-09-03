from app.extensions import db


class BundleItem(db.Model):

    __tablename__ = "bundle_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    bundle_id = db.Column(
        db.Integer,
        db.ForeignKey("bundles.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1
    )

    bundle = db.relationship(
        "Bundle",
        back_populates="items"
    )

    product = db.relationship(
        "Product"
    )

    def __repr__(self):
        return f"<BundleItem {self.id}>"