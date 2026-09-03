from datetime import datetime
import uuid

from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem

from app.cart import (
    get_cart_items,
    get_cart_subtotal,
    clear_cart,
)


# ============================================================
# ORDER NUMBER
# ============================================================

def generate_order_number():
    """
    Generate a unique Eagle Furniture order number.

    Example:
        EFN-20260826-9546A1
    """

    date_part = datetime.utcnow().strftime("%Y%m%d")
    unique_part = uuid.uuid4().hex[:6].upper()

    return f"EFN-{date_part}-{unique_part}"


# ============================================================
# CREATE ORDER FROM CART
# ============================================================

def create_order(
    customer_name,
    customer_phone,
    customer_email,
    county,
    town,
    delivery_address,
    payment_method,
    notes=None,
):
    """
    Convert the current shopping cart into a permanent
    database order.

    Returns:

        success, order, message
    """

    # --------------------------------------------------------
    # GET CART
    # --------------------------------------------------------

    cart_items = get_cart_items()

    if not cart_items:
        return (
            False,
            None,
            "Your cart is empty."
        )

    # --------------------------------------------------------
    # CLEAN CUSTOMER INFORMATION
    # --------------------------------------------------------

    customer_name = (customer_name or "").strip()
    customer_phone = (customer_phone or "").strip()
    customer_email = (customer_email or "").strip()
    county = (county or "").strip()
    town = (town or "").strip()
    delivery_address = (delivery_address or "").strip()
    payment_method = (payment_method or "").strip()
    notes = (notes or "").strip()

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not customer_name:
        return (
            False,
            None,
            "Please provide your full name."
        )

    if not customer_phone:
        return (
            False,
            None,
            "Please provide your phone number."
        )

    if not county:
        return (
            False,
            None,
            "Please provide your county."
        )

    if not town:
        return (
            False,
            None,
            "Please provide your town or area."
        )

    if not delivery_address:
        return (
            False,
            None,
            "Please provide your delivery address."
        )

    if not payment_method:
        return (
            False,
            None,
            "Please select a payment method."
        )

    # --------------------------------------------------------
    # CALCULATE TOTALS
    # --------------------------------------------------------

    subtotal = float(get_cart_subtotal())

    # Delivery is currently free / calculated later.
    delivery_fee = 0.0

    total = subtotal + delivery_fee

    # --------------------------------------------------------
    # CREATE ORDER
    # --------------------------------------------------------

    order = Order(
        order_number=generate_order_number(),

        customer_name=customer_name,

        customer_phone=customer_phone,

        customer_email=customer_email or None,

        county=county,

        town=town,

        delivery_address=delivery_address,

        payment_method=payment_method,

        payment_status="Pending",

        order_status="Pending",

        notes=notes or None,

        subtotal=subtotal,

        delivery_fee=delivery_fee,

        total=total,
    )

    db.session.add(order)

    # --------------------------------------------------------
    # CREATE ORDER ITEMS
    # --------------------------------------------------------
    #
    # IMPORTANT:
    # The OrderItem must be created INSIDE the loop.
    # This ensures every product in the cart is saved.
    #

    for item in cart_items:

        product = item["product"]

        order_item = OrderItem(
            order=order,

            product_id=product.id,

            product_name=product.name,

            quantity=int(item["quantity"]),

            unit_price=float(item["price"]),

            subtotal=float(item["subtotal"]),
        )

        db.session.add(order_item)

    # --------------------------------------------------------
    # SAVE DATABASE TRANSACTION
    # --------------------------------------------------------

    try:

        db.session.commit()

    except Exception as error:

        db.session.rollback()

        print(
            "ORDER CREATION ERROR:",
            error
        )

        return (
            False,
            None,
            "We could not complete your order. Please try again."
        )

    # --------------------------------------------------------
    # CLEAR CART
    # --------------------------------------------------------

    clear_cart()

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    return (
        True,
        order,
        "Your order has been placed successfully."
    )
