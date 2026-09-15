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



def get_sale_products():
    """
    Return active products currently on sale.
    """

    return (
        Product.query
        .filter(
            Product.active.is_(True),
            Product.sale_price.isnot(None),
            Product.sale_price > 0,
            Product.price.isnot(None),
            Product.sale_price < Product.price
        )
        .order_by(Product.created_at.desc())
        .all()
    )
   
# ============================================================
# HOME
# ============================================================
def build_showroom_department(
    key,
    name,
    description,
    category_slugs,
    subcategory_limit=5,
            products_per_subcategory=6,
):
    """Build populated, scalable showroom data from the database.

    Empty subcategories are excluded from the homepage. Collection pages
    remain unlimited and are handled by the dedicated collection route.
    """
    department_categories = []

    for category_slug in category_slugs:
        category = (
            Category.query
            .filter(
                Category.slug == category_slug,
                Category.active.is_(True),
            )
            .first()
        )
        if not category:
            continue

        subcategories = (
            Subcategory.query
            .filter(
                Subcategory.category_id == category.id,
                Subcategory.active.is_(True),
            )
            .order_by(
                Subcategory.display_order.asc(),
                Subcategory.name.asc(),
            )
            .all()
        )

        subcategory_data = []

        for subcategory in subcategories:
            products = (
                Product.query
                .filter(
                    Product.active.is_(True),
                    Product.category_id == category.id,
                    Product.subcategory_id == subcategory.id,
                    Product.image.isnot(None),
                    Product.image != "",
                )
                .order_by(
                    Product.featured.desc(),
                    Product.best_seller.desc(),
                    Product.created_at.desc(),
                )
                .all()
            )

            if not products:
                continue

            # Keep homepage sections curated, while collection pages stay
            # unlimited. Use the strongest products first.
            visible_products = products[:products_per_subcategory]

            image = subcategory.image
            if not image and visible_products:
                image = visible_products[0].image
            if not image:
                image = category.image

            subcategory_data.append({
                "subcategory": subcategory,
                "products": visible_products,
                "product_count": len(products),
                "image": image,
            })

            if len(subcategory_data) >= subcategory_limit:
                break

        if subcategory_data:
            department_categories.append({
                "category": category,
                "subcategory_data": subcategory_data,
            })

    return {
        "key": key,
        "name": name,
        "description": description,
        "categories": department_categories,
    }


@main.route("/")
def home():
    """Homepage showroom built entirely from the database."""

    # ---------------------------------------------------------
    # FEATURED PRODUCTS
    # ---------------------------------------------------------
    featured_products = (
        Product.query
        .filter(
            Product.active.is_(True),
            Product.featured.is_(True),
            Product.image.isnot(None),
            Product.image != "",
        )
        .order_by(Product.created_at.desc())
        .all()
    )

    # ---------------------------------------------------------
    # BEST SELLERS
    # ---------------------------------------------------------
    best_sellers = (
        Product.query
        .filter(
            Product.active.is_(True),
            Product.best_seller.is_(True),
            Product.image.isnot(None),
            Product.image != "",
        )
        .order_by(Product.created_at.desc())
        .all()
    )

    # ---------------------------------------------------------
    # NEW ARRIVALS
    # ---------------------------------------------------------
    new_arrivals = (
        Product.query
        .filter(
            Product.active.is_(True),
            Product.new_arrival.is_(True),
            Product.image.isnot(None),
            Product.image != "",
        )
        .order_by(Product.created_at.desc())
        .all()
    )

    # ---------------------------------------------------------
    # CURRENT OFFERS
    # ---------------------------------------------------------
    offers = (
        Product.query
        .filter(
            Product.active.is_(True),
            Product.image.isnot(None),
            Product.image != "",
            Product.sale_price.isnot(None),
            Product.sale_price > 0,
            Product.price.isnot(None),
            Product.sale_price < Product.price,
        )
        .order_by(Product.created_at.desc())
        .all()
    )

    # ---------------------------------------------------------
    # ACTIVE CATEGORIES
    # Used by homepage navigation and supporting sections.
    # ---------------------------------------------------------
    categories = (
        Category.query
        .filter(Category.active.is_(True))
        .order_by(
            Category.display_order.asc(),
            Category.name.asc(),
        )
        .all()
    )

    # Attach active subcategories without changing the database.
    for category in categories:
        category.home_subcategories = [
            subcategory
            for subcategory in category.subcategories
            if subcategory.active
        ]

    # ---------------------------------------------------------
    # FEATURED BUNDLES
    # ---------------------------------------------------------
    featured_bundles = [
        bundle
        for bundle in bundles
        if bundle.get("featured")
    ]

    # ---------------------------------------------------------
    # HOMEPAGE SHOWROOM DEPARTMENTS
    #
    # These are populated from the real database categories,
    # subcategories and products through build_showroom_department().
    #
    # Homepage products are curated.
    # Collection pages remain unlimited.
    # ---------------------------------------------------------
    showroom_departments = [

        build_showroom_department(
            key="living-room",
            name="Living Room",
            description=(
                "Discover bespoke sofas and living-room furniture "
                "designed for comfort, style and everyday living."
            ),
            category_slugs=[
                "sofas",
                "coffee-tables",
            ],
            subcategory_limit=5,
            products_per_subcategory=6,
        ),

        build_showroom_department(
            key="bedroom",
            name="Bedroom",
            description=(
                "Create a beautiful bedroom with custom beds, "
                "wardrobes and carefully selected bedroom furniture."
            ),
            category_slugs=[
                "beds",
                "wardrobes",
                "mattresses",
            ],
            subcategory_limit=5,
            products_per_subcategory=6,
        ),

        build_showroom_department(
            key="dining",
            name="Dining",
            description=(
                "Bring family and guests together around elegant "
                "dining sets made to suit your space."
            ),
            category_slugs=[
                "dining-sets",
            ],
            subcategory_limit=5,
            products_per_subcategory=6,
        ),

        build_showroom_department(
            key="entertainment",
            name="TV & Entertainment",
            description=(
                "Complete your entertainment space with modern TV "
                "units, wall-mounted designs and entertainment walls."
            ),
            category_slugs=[
                "tv-units",
            ],
            subcategory_limit=5,
            products_per_subcategory=6,
        ),

        build_showroom_department(
            key="office",
            name="Office Furniture",
            description=(
                "Professional office furniture designed for productive "
                "workspaces, businesses and modern offices."
            ),
            category_slugs=[
                "office-furniture",
            ],
            subcategory_limit=5,
            products_per_subcategory=6,
        ),

        build_showroom_department(
            key="outdoor",
            name="Outdoor Furniture",
            description=(
                "Upgrade your outdoor space with comfortable and "
                "stylish furniture made for relaxing and entertaining."
            ),
            category_slugs=[
                "outdoor-furniture",
            ],
            subcategory_limit=5,
            products_per_subcategory=6,
        ),
    ]

    # Remove departments where the database has no matching
    # active category/subcategory/product data.
    showroom_departments = [
        department
        for department in showroom_departments
        if department["categories"]
    ]

    return render_template(
        "pages/home.html",

        # Existing homepage data
        featured_products=featured_products,
        best_sellers=best_sellers,
        new_arrivals=new_arrivals,
        offers=offers,
        categories=categories,
        bundles=bundles,
        featured_bundles=featured_bundles,

        # Database-driven showroom data
        showroom_departments=showroom_departments,
    )


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
    """
    Display the individual product page.

    The selected product must be active.
    Related products and collection products are also limited
    to active products so legacy/deactivated records never
    appear on the storefront.
    """

    selected_product = (
        Product.query
        .filter(
            Product.id == product_id,
            Product.active.is_(True)
        )
        .first()
    )

    if selected_product is None:
        abort(404)

    # ---------------------------------------------------------
    # RELATED PRODUCTS
    # ---------------------------------------------------------
    #
    # Priority:
    # 1. Same subcategory
    # 2. Same category if no subcategory exists
    #
    # The current product is always excluded.
    #

    related_query = Product.query.filter(
        Product.id != selected_product.id,
        Product.active.is_(True)
    )

    if selected_product.subcategory_id:
        related_query = related_query.filter(
            Product.subcategory_id == selected_product.subcategory_id
        )

    elif selected_product.category_id:
        related_query = related_query.filter(
            Product.category_id == selected_product.category_id
        )

    related_products = (
        related_query
        .order_by(
            Product.featured.desc(),
            Product.best_seller.desc(),
            Product.created_at.desc()
        )
        .limit(4)
        .all()
    )

    # ---------------------------------------------------------
    # MORE PRODUCTS FROM SAME COLLECTION
    # ---------------------------------------------------------
    #
    # Additional active products from the same category.
    #
    # Products already shown in Related Products are excluded.
    #

    related_product_ids = [
        product.id for product in related_products
    ]

    collection_query = Product.query.filter(
        Product.id != selected_product.id,
        Product.active.is_(True)
    )

    if selected_product.category_id:
        collection_query = collection_query.filter(
            Product.category_id == selected_product.category_id
        )

    if related_product_ids:
        collection_query = collection_query.filter(
            ~Product.id.in_(related_product_ids)
        )

    collection_products = (
        collection_query
        .order_by(
            Product.featured.desc(),
            Product.best_seller.desc(),
            Product.created_at.desc()
        )
        .limit(12)
        .all()
    )

    # ---------------------------------------------------------
    # RENDER PRODUCT PAGE
    # ---------------------------------------------------------

    return render_template(
        "pages/product.html",
        product=selected_product,
        related_products=related_products,
        collection_products=collection_products,
    )

    # ---------------------------------------------------------
    # RELATED PRODUCTS
    # ---------------------------------------------------------
    #
    # Priority:
    # 1. Products from the same subcategory
    # 2. If no subcategory exists, products from same category
    #
    # The current product is always excluded.
    #

    related_query = Product.query.filter(
        Product.id != selected_product.id
    )

    if selected_product.subcategory_id:
        related_query = related_query.filter(
            Product.subcategory_id == selected_product.subcategory_id
        )
    elif selected_product.category_id:
        related_query = related_query.filter(
            Product.category_id == selected_product.category_id
        )

    related_products = (
        related_query
        .order_by(Product.created_at.desc())
        .limit(4)
        .all()
    )


    # ---------------------------------------------------------
    # MORE PRODUCTS FROM SAME COLLECTION
    # ---------------------------------------------------------
    #
    # These are additional products from the same category.
    #
    # Products already displayed in Related Products are
    # excluded so the customer does not see duplicate cards.
    #

    related_product_ids = [
        product.id for product in related_products
    ]

    collection_query = Product.query.filter(
        Product.id != selected_product.id
    )

    if selected_product.category_id:
        collection_query = collection_query.filter(
            Product.category_id == selected_product.category_id
        )

    if related_product_ids:
        collection_query = collection_query.filter(
            ~Product.id.in_(related_product_ids)
        )

    collection_products = (
        collection_query
        .order_by(Product.created_at.desc())
        .limit(12)
        .all()
    )


    # ---------------------------------------------------------
    # RENDER PRODUCT PAGE
    # ---------------------------------------------------------

    return render_template(
        "pages/product.html",
        product=selected_product,
        related_products=related_products,
        collection_products=collection_products,
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
# SUBCATEGORY COLLECTION
# ============================================================

@main.route("/collection/<slug>")
def collection(slug):
    selected_subcategory = (
        Subcategory.query
        .filter_by(slug=slug, active=True)
        .first()
    )

    if selected_subcategory is None:
        abort(404)

    products = (
        Product.query
        .filter(
            Product.subcategory_id == selected_subcategory.id,
            Product.image.isnot(None),
            Product.image != "",
        )
        .order_by(
            Product.featured.desc(),
            Product.best_seller.desc(),
            Product.created_at.desc(),
        )
        .all()
    )

    return render_template(
        "pages/collection.html",
        subcategory=selected_subcategory,
        category=selected_subcategory.category,
        products=products,
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

    site_url = current_app.config["SITE_URL"].rstrip("/")
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
    site_url + url_for(endpoint)
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
    site_url + url_for(
        "main.product",
        product_id=product.id
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
    site_url + url_for(
        "main.category",
        slug=category.slug
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


# ============================================================
# GOOGLE MERCHANT CENTER PRODUCT FEED
# ============================================================

@main.route("/merchant-feed.xml")
def merchant_feed():

    products = (
        Product.query
        .filter(
            Product.active.is_(True),
            Product.image.isnot(None),
            Product.image != "",
        )
        .order_by(Product.id.asc())
        .all()
    )

    site_url = current_app.config["SITE_URL"].rstrip("/")

    items = []

    for product in products:

        selling_price = (
            product.sale_price
            if product.sale_price is not None
            else product.price
        )

        if selling_price is None:
            continue

        product_url = f"{site_url}/product/{product.id}"
        image_url = f"{site_url}/static/{product.image}"

        title = product.name or ""
        description = (
            product.description
            or f"{product.name} from Eagle Furniture Ngara."
        )

        category_name = ""
        if product.category:
            category_name = product.category.name or ""

        items.append(
            f"""
            <item>
                <g:id>{escape_xml(str(product.id))}</g:id>
                <g:title>{escape_xml(title)}</g:title>
                <g:description>{escape_xml(description)}</g:description>
                <g:link>{escape_xml(product_url)}</g:link>
                <g:image_link>{escape_xml(image_url)}</g:image_link>
                <g:availability>in_stock</g:availability>
                <g:condition>new</g:condition>
                <g:price>{selling_price:.2f} KES</g:price>
                <g:brand>Eagle Furniture Ngara</g:brand>
                <g:product_type>{escape_xml(category_name)}</g:product_type>
            </item>
            """
        )

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:g="http://base.google.com/ns/1.0">

    <channel>

        <title>Eagle Furniture Ngara</title>

        <link>{escape_xml(site_url)}</link>

        <description>
            Furniture from Eagle Furniture Ngara, Nairobi, Kenya.
        </description>

        {''.join(items)}

    </channel>

</rss>
"""

    return Response(
        xml,
        mimetype="application/xml"
    )


# ============================================================
# XML ESCAPE HELPER
# ============================================================

def escape_xml(value):
    if value is None:
        return ""

    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )

