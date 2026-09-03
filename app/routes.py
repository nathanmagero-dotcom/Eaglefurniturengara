from flask import (
    Blueprint,
    Response,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from functools import wraps
from app.extensions import db

from app.models.order import Order
from app.models.product import Product
from app.models.subcategory import Subcategory
from app.models.category import Category

from app.orders import create_order

from app.cart import (
    add_to_cart,
    clear_cart,
    get_cart_count,
    get_cart_items,
    get_cart_subtotal,
    get_cart_total,
    remove_from_cart,
    update_cart,
)

from app.data.bundles import bundles
from app.data.products import products


# ============================================================
# BLUEPRINT
# ============================================================

main = Blueprint(
    "main",
    __name__,
)

# ============================================================
# ADMIN AUTHENTICATION
# ============================================================

def admin_required(view_function):
    """
    Protect admin routes.

    Users who are not logged in are redirected
    to the admin login page.
    """

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        if not session.get("admin_logged_in"):
            flash(
                "Please log in to access the admin dashboard.",
                "warning"
            )

            return redirect(
                url_for(
                    "main.admin_login",
                    next=request.url
                )
            )

        return view_function(*args, **kwargs)

    return wrapped_view
# ============================================================
# TEMPLATE CONTEXT
# ============================================================
# Makes cart_count available throughout the storefront.
#
# This means navbar.html, footer.html and other templates
# can use:
#
#     {{ cart_count }}
#
# without every route having to pass it manually.
# ============================================================

@main.app_context_processor
def inject_global_store_data():
    return {
        "cart_count": get_cart_count(),
    }


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_product(product_id):
    """
    Find a product by ID from the database.
    """

    return Product.query.get(product_id)


def find_category(slug):
    """
    Find an active category by slug.
    """

    return Category.query.filter_by(
        slug=slug,
        active=True
    ).first()


def find_bundle(bundle_id):
    """
    Find a furniture bundle by ID.
    """

    return next(
        (
            bundle
            for bundle in bundles
            if bundle.get("id") == bundle_id
        ),
        None,
    )


def get_product_price(product):

    price = product.price or 0
    sale_price = product.sale_price

    if (
        sale_price is not None
        and sale_price > 0
        and sale_price < price
    ):
        return sale_price

    return price

def search_products(query):
    """
    Search database products by name,
    description or category.
    """

    query = (query or "").strip()

    if not query:

        return (
            Product.query
            .order_by(
                Product.created_at.desc()
            )
            .all()
        )

    search_term = f"%{query}%"

    return (
        Product.query
        .outerjoin(
            Category,
            Product.category_id
            == Category.id
        )
        .filter(
            db.or_(
                Product.name.ilike(
                    search_term
                ),

                Product.description.ilike(
                    search_term
                ),

                Category.name.ilike(
                    search_term
                ),
            )
        )
        .order_by(
            Product.created_at.desc()
        )
        .all()
    )


def get_sale_products():
    """
    Return products currently on sale.
    """

    return (
        Product.query
        .filter(
            Product.sale_price.isnot(None),
            Product.sale_price > 0,
            Product.sale_price < Product.price
        )
        .order_by(Product.created_at.desc())
        .all()
    )
# ============================================================
# HOME
# ============================================================

@main.route("/")
def home():

    featured_products = (
    Product.query
    .filter(
        Product.featured.is_(True),
        Product.image.isnot(None),
        Product.image != ""
    )
    .order_by(Product.created_at.desc())
    .limit(8)
    .all()
)
    best_sellers = (
        Product.query
        .filter_by(best_seller=True)
        .order_by(Product.created_at.desc())
        .limit(6)
        .all()
    )

    new_arrivals = (
        Product.query
        .filter_by(new_arrival=True)
        .order_by(Product.created_at.desc())
        .limit(6)
        .all()
    )

    offers = (
        Product.query
        .filter(
            Product.sale_price.isnot(None),
            Product.sale_price > 0,
            Product.sale_price < Product.price
        )
        .order_by(Product.created_at.desc())
        .limit(6)
        .all()
    )

    category_list = (
        Category.query
        .filter_by(active=True)
        .order_by(Category.display_order.asc())
        .all()
    )

    return render_template(
        "pages/home.html",
        featured_products=featured_products,
        best_sellers=best_sellers,
        new_arrivals=new_arrivals,
        offers=offers,
        categories=category_list,
        bundles=bundles,
    )


    # ============================================================
# SHOP
# ============================================================

@main.route("/shop")
@main.route("/products")
def shop():

    # --------------------------------------------------------
    # GET FILTERS
    # --------------------------------------------------------

    search = request.args.get(
        "search",
        ""
    ).strip()

    category_filter = request.args.get(
        "category",
        ""
    ).strip()

    subcategory_filter = request.args.get(
        "subcategory",
        ""
    ).strip()

    sort = request.args.get(
        "sort",
        ""
    ).strip()


    # --------------------------------------------------------
    # BASE PRODUCT QUERY
    # --------------------------------------------------------

    query = Product.query


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if search:
        search_term = f"%{search}%"

        query = query.filter(
            db.or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
                Product.category.has(Category.name.ilike(search_term)),
                Product.subcategory.has(Subcategory.name.ilike(search_term)),
            )
        )
    # --------------------------------------------------------
    # SELECTED CATEGORY
    # --------------------------------------------------------

    selected_category = None

    if category_filter:

        selected_category = (
            Category.query
            .filter_by(
                slug=category_filter,
                active=True
            )
            .first()
        )

        if selected_category:

            query = query.filter(
                Product.category_id
                == selected_category.id
            )


    # --------------------------------------------------------
    # SELECTED SUBCATEGORY
    # --------------------------------------------------------

    selected_subcategory = None

    if subcategory_filter:

        selected_subcategory = (
            Subcategory.query
            .filter_by(
                slug=subcategory_filter,
                active=True
            )
            .first()
        )

        if selected_subcategory:

            # ------------------------------------------------
            # Make sure the selected subcategory belongs to
            # the selected category when a category is chosen.
            # ------------------------------------------------

            if (
                selected_category is None
                or selected_subcategory.category_id
                == selected_category.id
            ):

                query = query.filter(
                    Product.subcategory_id
                    == selected_subcategory.id
                )


    # --------------------------------------------------------
    # SORTING
    # --------------------------------------------------------

    if sort == "price_low":

        query = query.order_by(
            Product.price.asc()
        )

    elif sort == "price_high":

        query = query.order_by(
            Product.price.desc()
        )

    elif sort == "name":

        query = query.order_by(
            Product.name.asc()
        )

    elif sort == "best_selling":

        query = (
            query
            .filter(
                Product.best_seller.is_(True)
            )
            .order_by(
                Product.created_at.desc()
            )
        )

    elif sort == "newest":

        query = query.order_by(
            Product.created_at.desc()
        )

    else:

        query = (
        query
        .outerjoin(
            Category,
            Product.category_id == Category.id
        )
        .order_by(
            db.case(
                (Category.slug == "sofas", 0),
                else_=1
            ),
            Product.created_at.desc()
        )
    )


    # --------------------------------------------------------
    # PRODUCTS
    # --------------------------------------------------------

    products = query.all()


    # --------------------------------------------------------
    # ACTIVE CATEGORIES
    # --------------------------------------------------------

    categories = (
        Category.query
        .filter_by(
            active=True
        )
        .order_by(
            Category.display_order.asc()
        )
        .all()
    )


    # --------------------------------------------------------
    # ACTIVE SUBCATEGORIES
    # --------------------------------------------------------

    subcategories = (
        Subcategory.query
        .filter_by(
            active=True
        )
        .order_by(
            Subcategory.display_order.asc()
        )
        .all()
    )


    # --------------------------------------------------------
    # CATEGORY-SPECIFIC SUBCATEGORIES
    # --------------------------------------------------------

    selected_subcategories = []

    if selected_category:

        selected_subcategories = [
            subcategory
            for subcategory
            in selected_category.subcategories
            if subcategory.active
        ]


    # --------------------------------------------------------
    # BUNDLES
    # --------------------------------------------------------

    shop_bundles = bundles


    # --------------------------------------------------------
    # RENDER SHOP
    # --------------------------------------------------------

    return render_template(

        "pages/shop.html",

        products=products,

        bundles=shop_bundles,

        categories=categories,

        subcategories=subcategories,

        selected_subcategories=selected_subcategories,

        selected_category=selected_category,

        selected_subcategory=selected_subcategory,

        search=search,

        selected_category_slug=category_filter,

        selected_subcategory_slug=subcategory_filter,

        selected_sort=sort,

    )
    # --------------------------------------------------------
    # BASE PRODUCT QUERY
    # --------------------------------------------------------

    query = (
        Product.query
        .outerjoin(
            Category,
            Product.category_id == Category.id
        )
    )

# ============================================================
# PRODUCT DETAILS
# ============================================================

@main.route("/product/<int:product_id>")
def product(product_id):

    selected_product = find_product(
        product_id
    )

    if selected_product is None:
        abort(404)

    related_products = (
        Product.query
        .filter(
            Product.category_id
            == selected_product.category_id,

            Product.id
            != selected_product.id,
        )
        .order_by(
            Product.created_at.desc()
        )
        .limit(4)
        .all()
    )

    return render_template(
        "pages/product.html",

        product=selected_product,

        related_products=related_products,
    )
# ============================================================
# CATEGORIES
# ============================================================

@main.route("/categories")
def category_list():

    category_list = (
        Category.query
        .filter_by(
            active=True
        )
        .order_by(
            Category.display_order.asc()
        )
        .all()
    )

    return render_template(
        "pages/categories.html",
        categories=category_list,
    )


# ============================================================
# SINGLE CATEGORY
# ============================================================

@main.route("/category/<slug>")
def category(slug):

    selected_category = find_category(
        slug
    )

    if selected_category is None:
        abort(404)

    category_products = (
        Product.query
        .filter_by(
            category_id=selected_category.id
        )
        .order_by(
            Product.created_at.desc()
        )
        .all()
    )

    return render_template(
        "pages/category.html",

        category=selected_category,

        products=category_products,
    )

# ============================================================
# BUNDLES / FURNITURE PACKAGES
# ============================================================

@main.route("/bundles")
def bundle_list():

    return render_template(
        "pages/bundles.html",
        bundles=bundles,
    )


@main.route("/bundle/<int:bundle_id>")
def bundle(bundle_id):

    selected_bundle = find_bundle(bundle_id)

    if selected_bundle is None:
        abort(404)

    related_bundles = [
        item
        for item in bundles
        if item.get("id")
        != selected_bundle.get("id")
    ][:3]

    return render_template(
        "pages/bundle.html",
        bundle=selected_bundle,
        related_bundles=related_bundles,
    )


# ============================================================
# OFFERS
# ============================================================

@main.route("/offers")
def offers():

    return render_template(
        "pages/offers.html",
        offers=get_sale_products(),
    )


# ============================================================
# CART
# ============================================================

@main.route("/cart")
def cart():

    from flask import session

    print("\n==============================")
    print("CART DEBUG")
    print("==============================")

    print("SESSION:")
    print(dict(session))

    print("CART ITEMS:")
    print(get_cart_items())

    print("CART COUNT:")
    print(get_cart_count())

    print("CART SUBTOTAL:")
    print(get_cart_subtotal())

    print("==============================\n")

    items = get_cart_items()
    subtotal = get_cart_subtotal()
    total = get_cart_total()
    cart_count = get_cart_count()

    return render_template(
        "pages/cart.html",
        items=items,
        subtotal=subtotal,
        total=total,
        cart_count=cart_count,
    )

# ============================================================
# ADD PRODUCT TO CART
# ============================================================

@main.route(
    "/cart/add/<int:product_id>",
    methods=["POST"],
)
def add_product_to_cart(product_id):

    quantity = request.form.get(
        "quantity",
        1,
        type=int,
    )

    if quantity < 1:
        quantity = 1

    success, message = add_to_cart(
        product_id=product_id,
        quantity=quantity,
    )

    if success:

        flash(
            message,
            "success",
        )

        return redirect(
            url_for("main.cart")
        )

    flash(
        message,
        "danger",
    )

    return redirect(
        request.referrer
        or url_for("main.shop")
    )
# ============================================================
# UPDATE CART
# ============================================================

@main.route(
    "/cart/update/<int:product_id>",
    methods=["POST"],
)
def update_product_cart(product_id):

    quantity = request.form.get(
        "quantity",
        1,
        type=int,
    )

    success, message = update_cart(
        product_id=product_id,
        quantity=quantity,
    )

    if success:
        flash(
            message,
            "success",
        )
    else:
        flash(
            message,
            "danger",
        )

    return redirect(
        url_for("main.cart")
    )


# ============================================================
# REMOVE FROM CART
# ============================================================

@main.route(
    "/cart/remove/<int:product_id>",
    methods=["POST"],
)
def remove_product_from_cart(product_id):

    success, message = remove_from_cart(
        product_id
    )

    if success:
        flash(
            message,
            "success",
        )
    else:
        flash(
            message,
            "danger",
        )

    return redirect(
        url_for("main.cart")
    )


# ============================================================
# CLEAR CART
# ============================================================

@main.route(
    "/cart/clear",
    methods=["POST"],
)
def clear_shopping_cart():

    clear_cart()

    flash(
        "Your cart has been cleared.",
        "success",
    )

    return redirect(
        url_for("main.cart")
    )


# ============================================================
# CHECKOUT
# ============================================================

@main.route("/checkout", methods=["GET", "POST"])
def checkout():

    # --------------------------------------------------------
    # GET CART
    # --------------------------------------------------------

    items = get_cart_items()

    subtotal = get_cart_subtotal()

    total = get_cart_total()

    cart_count = get_cart_count()


    # --------------------------------------------------------
    # EMPTY CART
    # --------------------------------------------------------

    if not items:

        flash(
            "Your cart is empty. Please add a product before checkout.",
            "warning",
        )

        return redirect(
            url_for("main.shop")
        )


    # --------------------------------------------------------
    # SUBMIT ORDER
    # --------------------------------------------------------

    if request.method == "POST":

        customer_name = request.form.get(
            "customer_name",
            ""
        )

        customer_phone = request.form.get(
            "customer_phone",
            ""
        )

        customer_email = request.form.get(
            "customer_email",
            ""
        )

        county = request.form.get(
            "county",
            ""
        )

        town = request.form.get(
            "town",
            ""
        )

        delivery_address = request.form.get(
            "delivery_address",
            ""
        )

        payment_method = request.form.get(
            "payment_method",
            ""
        )

        notes = request.form.get(
            "notes",
            ""
        )


        # ----------------------------------------------------
        # CREATE ORDER
        # ----------------------------------------------------

        success, order, message = create_order(

            customer_name=customer_name,

            customer_phone=customer_phone,

            customer_email=customer_email,

            county=county,

            town=town,

            delivery_address=delivery_address,

            payment_method=payment_method,

            notes=notes,
        )


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if success:

            flash(
                message,
                "success",
            )

            return redirect(
                url_for(
                    "main.order_confirmation",
                    order_number=order.order_number,
                )
            )


        # ----------------------------------------------------
        # FAILURE
        # ----------------------------------------------------

        flash(
            message,
            "danger",
        )


    # --------------------------------------------------------
    # CHECKOUT PAGE
    # --------------------------------------------------------

    return render_template(

        "pages/checkout.html",

        items=items,

        subtotal=subtotal,

        total=total,

        cart_count=cart_count,

    )


# ============================================================
# ORDER CONFIRMATION
# ============================================================

@main.route(
    "/order-confirmation/<order_number>"
)
def order_confirmation(order_number):

    order = Order.query.filter_by(
        order_number=order_number
    ).first_or_404()


    return render_template(

        "pages/order_confirmation.html",

        order=order,

    )

# ============================================================
# QUOTE
# ============================================================

@main.route("/quote")
def quote():

    return render_template(
        "pages/quote.html"
    )


@main.route("/quote/success")
def quote_success():

    return render_template(
        "pages/quote_success.html"
    )

# ============================================================
# WISHLIST
# ============================================================

@main.route("/wishlist")
def wishlist():

    return render_template(
        "pages/wishlist.html"
    )


# ============================================================
# COMPARE
# ============================================================

@main.route("/compare")
def compare():

    return render_template(
        "pages/compare.html"
    )


# ============================================================
# SEARCH RESULTS
# ============================================================

# ============================================================
# SEARCH RESULTS
# ============================================================

@main.route("/search")
def search_results():

    query = request.args.get(
        "q",
        "",
    ).strip()

    results = search_products(
        query
    )

    return render_template(
        "pages/search.html",

        query=query,

        results=results,
    )

# ============================================================
# ABOUT
# ============================================================

@main.route("/about")
def about():

    return render_template(
        "pages/about.html"
    )


# ============================================================
# CONTACT
# ============================================================

@main.route("/contact")
def contact():

    return render_template(
        "pages/contact.html"
    )


# ============================================================
# GALLERY
# ============================================================
@main.route("/gallery")
def gallery():

    gallery_products = []

    for product in products:

        images = product.get("gallery", [])

        # If gallery is empty, use the main product image
        if not images and product.get("image"):
            images = [product["image"]]

        for image in images:

            gallery_products.append({
                "image": image,
                "name": product.get("name"),
                "category": product.get("category"),
                "subcategory": product.get("subcategory"),
                "product_id": product.get("id"),
            })

    return render_template(
        "pages/gallery.html",
        gallery_products=gallery_products
    )


# ============================================================
# REVIEWS
# ============================================================

@main.route("/reviews")
def reviews():

    return render_template(
        "pages/reviews.html"
    )


# ============================================================
# BLOG
# ============================================================

@main.route("/blog")
def blog():

    return render_template(
        "pages/blog.html"
    )


@main.route("/blog/<slug>")
def blog_post(slug):

    return render_template(
        "pages/blog_post.html",
        slug=slug,
    )


# ============================================================
# FAQ
# ============================================================

@main.route("/faq")
def faq():

    return render_template(
        "pages/faq.html"
    )


# ============================================================
# DELIVERY
# ============================================================

@main.route("/delivery")
def delivery():

    return render_template(
        "pages/delivery.html"
    )


# ============================================================
# PAYMENT
# ============================================================

@main.route("/payment")
def payment():

    return render_template(
        "pages/payment.html"
    )


# ============================================================
# RETURNS
# ============================================================

@main.route("/returns")
def returns():

    return render_template(
        "pages/returns.html"
    )


# ============================================================
# PRIVACY
# ============================================================

@main.route("/privacy")
def privacy():

    return render_template(
        "pages/privacy.html"
    )


# ============================================================
# TERMS
# ============================================================

@main.route("/terms")
def terms():

    return render_template(
        "pages/terms.html"
    )


# ============================================================
# CUSTOM FURNITURE
# ============================================================

@main.route("/custom-furniture")
def custom_furniture():

    return render_template(
        "pages/custom_furniture.html"
    )


# ============================================================
# INTERIOR DESIGN
# ============================================================

@main.route("/interior-design")
def interior_design():

    return render_template(
        "pages/interior_design.html"
    )


# ============================================================
# OFFICE FURNITURE
# ============================================================

@main.route("/office-furniture")
def office_furniture():

    return render_template(
        "pages/office_furniture.html"
    )


# ============================================================
# AIRBNB PACKAGES
# ============================================================

@main.route("/airbnb-packages")
def airbnb_packages():

    return render_template(
        "pages/airbnb_packages.html"
    )


# ============================================================
# API — SEARCH
# ============================================================

@main.route("/api/search")
def api_search():

    query = request.args.get(
        "q",
        "",
    ).strip()

    return jsonify(
        search_products(query)
    )


# ============================================================
# API — PRODUCTS
# ============================================================

# ============================================================
# API — PRODUCTS
# ============================================================

@main.route("/api/products")
def api_products():

    products = (
        Product.query
        .order_by(
            Product.created_at.desc()
        )
        .all()
    )

    return jsonify([
        {
            "id": product.id,

            "name": product.name,

            "description": product.description,

            "price": product.price,

            "sale_price": product.sale_price,

            "category_id": product.category_id,

            "category": (
                product.category.name
                if product.category
                else None
            ),
        }

        for product in products
    ])

# ============================================================
# API — CATEGORIES
# ============================================================

# ============================================================
# API — CATEGORIES
# ============================================================

@main.route("/api/categories")
def api_categories():

    category_list = (
        Category.query
        .filter_by(
            active=True
        )
        .order_by(
            Category.display_order.asc()
        )
        .all()
    )

    return jsonify([

        {
            "id": category.id,

            "name": category.name,

            "slug": category.slug,

            "product_count": len(
                category.products
            ),
        }

        for category in category_list

    ])
# ============================================================
# API — FEATURED
# ============================================================

# ============================================================
# API — FEATURED
# ============================================================

@main.route("/api/featured")
def api_featured():

    products = (
        Product.query
        .filter_by(
            featured=True
        )
        .order_by(
            Product.created_at.desc()
        )
        .all()
    )

    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "sale_price": product.sale_price,
        }

        for product in products
    ])

# ============================================================
# API — BEST SELLERS
# ============================================================

# ============================================================
# API — BEST SELLERS
# ============================================================

@main.route("/api/best-sellers")
def api_best_sellers():

    products = (
        Product.query
        .filter_by(
            best_seller=True
        )
        .order_by(
            Product.created_at.desc()
        )
        .all()
    )

    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "sale_price": product.sale_price,
        }

        for product in products
    ])

# ============================================================
# API — NEW ARRIVALS
# ============================================================

# ============================================================
# API — NEW ARRIVALS
# ============================================================

@main.route("/api/new-arrivals")
def api_new_arrivals():

    products = (
        Product.query
        .filter_by(
            new_arrival=True
        )
        .order_by(
            Product.created_at.desc()
        )
        .all()
    )

    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "sale_price": product.sale_price,
        }

        for product in products
    ])

# ============================================================
# API — FEATURED BUNDLES
# ============================================================

@main.route("/api/featured-bundles")
def api_featured_bundles():

    featured = [
        bundle
        for bundle in bundles
        if bundle.get("featured")
    ]

    return jsonify(featured)


# ============================================================
# API — STATS
# ============================================================

@main.route("/api/stats")
def api_stats():

    return jsonify({

        "products": Product.query.count(),

        "categories": (
            Category.query
            .filter_by(active=True)
            .count()
        ),

        "bundles": len(bundles),

    })


# ============================================================
# ADMIN LOGIN
# ============================================================

@main.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if session.get("admin_logged_in"):
        return redirect(
            url_for("main.dashboard")
        )

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        admin_username = current_app.config.get(
            "ADMIN_USERNAME",
            "admin"
        )

        admin_password = current_app.config.get(
            "ADMIN_PASSWORD",
            ""
        )

        if (
            username == admin_username
            and password == admin_password
        ):

            session.clear()

            session["admin_logged_in"] = True
            session["admin_username"] = username

            next_url = request.args.get("next")

            if (
                next_url
                and next_url.startswith("/")
            ):
                return redirect(next_url)

            return redirect(
                url_for("main.dashboard")
            )

        flash(
            "Invalid username or password.",
            "danger"
        )

    return render_template(
        "admin/login.html"
    )  

# ============================================================
# ADMIN LOGOUT
# ============================================================

@main.route("/admin/logout")
def admin_logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("main.admin_login")
    )  

# ============================================================
# ADMIN — TEMPORARY STOREFRONT ADMIN
# ============================================================
# These routes are kept for the current project structure.
# They can later be moved into a dedicated admin blueprint
# without changing the public storefront URLs.
# ============================================================

@main.route("/admin")
@admin_required
def dashboard():
    total_orders = Order.query.count()

    pending_orders = Order.query.filter(
        Order.order_status == "Pending"
    ).count()

    paid_orders = Order.query.filter(
        Order.payment_status == "Paid"
    ).count()

    delivered_orders = Order.query.filter(
        Order.order_status == "Delivered"
    ).count()

    total_sales = db.session.query(
        db.func.coalesce(
            db.func.sum(Order.total),
            0
        )
    ).filter(
        Order.payment_status == "Paid"
    ).scalar()

    return render_template(
        "admin/dashboard.html",

        total_products=Product.query.count(),

        total_categories=Category.query.filter_by(
            active=True
        ).count(),

        total_bundles=len(bundles),

        total_orders=total_orders,

        pending_orders=pending_orders,

        paid_orders=paid_orders,

        delivered_orders=delivered_orders,

        total_sales=total_sales,
    )

@main.route("/admin/products")
@admin_required
def admin_products():

    return render_template(
        "admin/products.html"
    )


@main.route("/admin/categories")
@admin_required
def admin_categories():

    return render_template(
        "admin/categories.html"
    )


@main.route("/admin/bundles")
@admin_required
def admin_bundles():

    return render_template(
        "admin/bundles.html"
    )


from sqlalchemy import or_

@main.route("/admin/orders")
@admin_required
def admin_orders():

    search = request.args.get("search", "").strip()
    order_status = request.args.get("order_status", "").strip()
    payment_status = request.args.get("payment_status", "").strip()

    query = Order.query.order_by(Order.created_at.desc())

    # ----------------------------------------
    # SEARCH
    # ----------------------------------------
    if search:
        search_term = f"%{search}%"

        query = query.filter(
            or_(
                Order.order_number.ilike(search_term),
                Order.customer_name.ilike(search_term),
                Order.customer_phone.ilike(search_term),
            )
        )

    # ----------------------------------------
    # FILTER: ORDER STATUS
    # ----------------------------------------
    if order_status:
        query = query.filter(Order.order_status == order_status)

    # ----------------------------------------
    # FILTER: PAYMENT STATUS
    # ----------------------------------------
    if payment_status:
        query = query.filter(Order.payment_status == payment_status)

    orders = query.all()

    return render_template(
        "admin/orders.html",
        orders=orders,
        search=search,
        order_status=order_status,
        payment_status=payment_status,
    )

@main.route("/admin/orders/<int:order_id>")
@admin_required
def admin_order_detail(order_id):
    from app.models.order import Order

    order = Order.query.get_or_404(order_id)

    return render_template(
        "admin/order_detail.html",
        order=order
    )

@main.route(
    "/admin/orders/<int:order_id>/update",
    methods=["POST"]
)
@admin_required
def admin_order_update(order_id):

    from flask import request, redirect, url_for, flash
    from app.models.order import Order

    order = Order.query.get_or_404(order_id)

    order_status = request.form.get(
        "order_status",
        ""
    ).strip()

    payment_status = request.form.get(
        "payment_status",
        ""
    ).strip()

    allowed_order_statuses = [
        "Pending",
        "Confirmed",
        "Processing",
        "Ready for Delivery",
        "Delivered",
        "Cancelled",
    ]

    allowed_payment_statuses = [
        "Pending",
        "Paid",
        "Failed",
        "Refunded",
    ]

    if order_status in allowed_order_statuses:
        order.order_status = order_status

    if payment_status in allowed_payment_statuses:
        order.payment_status = payment_status

    db.session.commit()

    flash(
        f"Order {order.order_number} updated successfully.",
        "success"
    )

    return redirect(
        url_for(
            "main.admin_order_detail",
            order_id=order.id
        )
    )


# ============================================================
# SEO — XML SITEMAP
# ============================================================

@main.route("/sitemap.xml")
def sitemap():

    urls = []

    # --------------------------------------------------------
    # STATIC PUBLIC PAGES
    # --------------------------------------------------------

    static_endpoints = [
        "main.home",
        "main.shop",
        "main.category_list",
        "main.bundle_list",
        "main.offers",
        "main.quote",
        "main.about",
        "main.contact",
        "main.gallery",
        "main.reviews",
        "main.blog",
        "main.faq",
        "main.delivery",
        "main.payment",
        "main.returns",
        "main.privacy",
        "main.terms",
        "main.custom_furniture",
        "main.interior_design",
        "main.office_furniture",
        "main.airbnb_packages",
    ]

    for endpoint in static_endpoints:

        try:

            urls.append(
                url_for(
                    endpoint,
                    _external=True
                )
            )

        except Exception:

            pass

    # --------------------------------------------------------
    # PRODUCT PAGES
    # --------------------------------------------------------

    products = (
        Product.query
        .order_by(Product.id.asc())
        .all()
    )

    for product in products:

        urls.append(
            url_for(
                "main.product",
                product_id=product.id,
                _external=True
            )
        )

    # --------------------------------------------------------
    # CATEGORY PAGES
    # --------------------------------------------------------

    categories = (
        Category.query
        .filter_by(active=True)
        .order_by(Category.display_order.asc())
        .all()
    )

    for category in categories:

        urls.append(
            url_for(
                "main.category",
                slug=category.slug,
                _external=True
            )
        )

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    urls = list(dict.fromkeys(urls))

    # --------------------------------------------------------
    # BUILD XML
    # --------------------------------------------------------

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for page_url in urls:

        xml.append(
            "    <url>"
        )

        xml.append(
            f"        <loc>{page_url}</loc>"
        )

        xml.append(
            "    </url>"
        )

    xml.append("</urlset>")

    return Response(
        "\n".join(xml),
        mimetype="application/xml"
    )

# ============================================================
# SEO — ROBOTS.TXT
# ============================================================

@main.route("/robots.txt")
def robots():

    sitemap_url = (
        current_app.config["SITE_URL"].rstrip("/")
        + "/sitemap.xml"
    )

    robots_content = """User-agent: *
Allow: /

Disallow: /admin/
Disallow: /cart
Disallow: /checkout
Disallow: /order-confirmation/
Disallow: /wishlist
Disallow: /compare
Disallow: /api/

Sitemap: """ + sitemap_url

    return robots_content, 200, {
        "Content-Type": "text/plain"
    }
# ============================================================
# 404 ERROR
# ============================================================

@main.app_errorhandler(404)
def page_not_found(error):

    return render_template(
        "pages/404.html"
    ), 404

