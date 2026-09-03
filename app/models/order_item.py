from app.extensions import db


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "orders.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "products.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    product_name = db.Column(
        db.String(150),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    unit_price = db.Column(
        db.Float,
        nullable=False
    )

    subtotal = db.Column(
        db.Float,
        nullable=False
    )

    order = db.relationship(
        "Order",
        back_populates="items"
    )

    product = db.relationship(
        "Product"
    )

    def __repr__(self):
        return f"<OrderItem {self.product_name}>"