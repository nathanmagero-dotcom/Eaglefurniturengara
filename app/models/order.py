from datetime import datetime

from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )

    customer_name = db.Column(
        db.String(150),
        nullable=False
    )

    customer_phone = db.Column(
        db.String(30),
        nullable=False
    )

    customer_email = db.Column(
        db.String(150),
        nullable=True
    )

    county = db.Column(
        db.String(100),
        nullable=False
    )

    town = db.Column(
        db.String(100),
        nullable=False
    )

    delivery_address = db.Column(
        db.String(255),
        nullable=False
    )

    payment_method = db.Column(
        db.String(50),
        nullable=False,
        default="M-Pesa"
    )

    payment_status = db.Column(
        db.String(50),
        nullable=False,
        default="Pending"
    )

    order_status = db.Column(
        db.String(50),
        nullable=False,
        default="Pending"
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    subtotal = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    delivery_fee = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    total = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Order {self.order_number}>"