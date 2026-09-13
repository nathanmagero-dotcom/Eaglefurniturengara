from app import create_app
from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.subcategory import Subcategory
from slugify import slugify

app = create_app()
app.app_context().push()


def get_category(name):
    return Category.query.filter_by(name=name).first()


def get_subcategory(name):
    return Subcategory.query.filter_by(name=name).first()


def add_product(data):
    existing = Product.query.filter_by(sku=data["sku"]).first()
    if existing:
        print(f"SKIPPED (exists): {data['name']}")
        return

    product = Product(
        name=data["name"],
        slug=slugify(data["name"]),
        sku=data["sku"],
        price=data["price"],
        sale_price=data.get("sale_price"),
        description=data["description"],
        category_id=data["category_id"],
        subcategory_id=data["subcategory_id"],
        image=data["image"],
        active=True,
        featured=True,
        best_seller=False,
        new_arrival=True,
    )

    db.session.add(product)
    print(f"ADDED: {data['name']}")


# --------------------------------------------------
# PRODUCTS
# --------------------------------------------------

sofa_cat = get_category("Sofas")
bed_cat = get_category("Beds")
dining_cat = get_category("Dining Sets")

products = [

    {
        "name": "Modern 3-Seater Sofa",
        "sku": "SOF007",
        "price": 64999,
        "sale_price": 54999,
        "description": "Modern 3-seater sofa with premium fabric, deep cushions, and a sleek contemporary finish. Customizable in fabric and color.",
        "category_id": sofa_cat.id,
        "subcategory_id": get_subcategory("Modern Sofas").id,
        "image": "images/products/sofas/modern-3-seater.jpg",
    },

    {
        "name": "Solid Wood Dining Table",
        "sku": "DIN005",
        "price": 34999,
        "sale_price": None,
        "description": "Solid hardwood dining table crafted for durability and timeless style. Suitable for modern and classic interiors.",
        "category_id": dining_cat.id,
        "subcategory_id": get_subcategory("Dining").id,
        "image": "images/products/dining/solid-wood-table.jpg",
    },

    {
        "name": "Queen Bed Frame",
        "sku": "BED005",
        "price": 36999,
        "sale_price": 29999,
        "description": "Elegant queen bed frame with strong structure and refined finish. Fully customizable design, color, and fabric options.",
        "category_id": bed_cat.id,
        "subcategory_id": get_subcategory("Queen").id,
        "image": "images/products/beds/queen-bed-frame.jpg",
    },
]


# --------------------------------------------------
# EXECUTE
# --------------------------------------------------

for p in products:
    add_product(p)

db.session.commit()

print("\nDONE: New products added successfully.")