from flask import session

from app.models.product import Product


# ============================================================
# CART STORAGE
# ============================================================

CART_SESSION_KEY = "shopping_cart"


# ============================================================
# INTERNAL HELPERS
# ============================================================

def _get_cart():
    """
    Return the current shopping cart.

    Cart format:

    {
        "1": 2,
        "5": 1
    }

    Key   = product ID
    Value = quantity
    """

    cart = session.get(CART_SESSION_KEY, {})

    if not isinstance(cart, dict):
        cart = {}

    return cart


def _save_cart(cart):
    """
    Save the cart back into the Flask session.
    """

    session[CART_SESSION_KEY] = cart
    session.modified = True


def _find_product(product_id):
    """
    Find a product from the database.
    """

    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return None

    return Product.query.get(product_id)


def _get_product_price(product):
    """
    Return the current product selling price.
    """

    if product is None:
        return 0.0

    try:
        return float(product.price or 0)
    except (TypeError, ValueError):
        return 0.0


# ============================================================
# CART ITEMS
# ============================================================

def get_cart_items():
    """
    Return complete cart items.

    Each item contains:

        product
        quantity
        price
        subtotal
    """

    cart = _get_cart()

    items = []

    for product_id, quantity in cart.items():

        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue

        if quantity <= 0:
            continue

        product = _find_product(product_id)

        if product is None:
            continue

        price = _get_product_price(product)

        items.append({
            "product": product,
            "quantity": quantity,
            "price": price,
            "subtotal": price * quantity,
        })

    return items


# ============================================================
# CART COUNT
# ============================================================

def get_cart_count():
    """
    Return total number of products in the cart.
    """

    cart = _get_cart()

    total_quantity = 0

    for quantity in cart.values():

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue

        if quantity > 0:
            total_quantity += quantity

    return total_quantity


# ============================================================
# CART SUBTOTAL
# ============================================================

def get_cart_subtotal():
    """
    Calculate cart subtotal.
    """

    return sum(
        item["subtotal"]
        for item in get_cart_items()
    )


# ============================================================
# CART TOTAL
# ============================================================

def get_cart_total():
    """
    Calculate current cart total.

    Delivery will be added during checkout.
    """

    return get_cart_subtotal()


# ============================================================
# ADD TO CART
# ============================================================

def add_to_cart(product_id, quantity=1):
    """
    Add a database product to the shopping cart.
    """

    product = _find_product(product_id)

    if product is None:
        return False, "Product not found."

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart = _get_cart()

    key = str(product.id)

    current_quantity = cart.get(key, 0)

    try:
        current_quantity = int(current_quantity)
    except (TypeError, ValueError):
        current_quantity = 0

    new_quantity = current_quantity + quantity

    cart[key] = new_quantity

    _save_cart(cart)

    return (
        True,
        f"{product.name} added to your cart."
    )


# ============================================================
# UPDATE CART
# ============================================================

def update_cart(product_id, quantity):
    """
    Update the quantity of an existing cart item.
    """

    product = _find_product(product_id)

    if product is None:
        return False, "Product not found."

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return False, "Invalid quantity."

    cart = _get_cart()

    key = str(product.id)

    if key not in cart:
        return False, "Product is not in your cart."

    if quantity <= 0:

        cart.pop(key, None)

        _save_cart(cart)

        return True, "Product removed from your cart."

    cart[key] = quantity

    _save_cart(cart)

    return True, "Cart updated successfully."


# ============================================================
# REMOVE FROM CART
# ============================================================

def remove_from_cart(product_id):
    """
    Remove a product completely from the cart.
    """

    cart = _get_cart()

    key = str(product_id)

    if key not in cart:
        return False, "Product is not in your cart."

    cart.pop(key)

    _save_cart(cart)

    return True, "Product removed from your cart."


# ============================================================
# CLEAR CART
# ============================================================

def clear_cart():
    """
    Remove all products from the cart.
    """

    session.pop(CART_SESSION_KEY, None)

    session.modified = True