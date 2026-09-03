from app import create_app
from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.subcategory import Subcategory

app = create_app()

products_to_add = [
    {
        "name": "U-Shaped Family Sofa",
        "slug": "u-shaped-family-sofa",
        "category": "Sofas",
        "subcategory": "U-Shaped",
        "price": 118000,
        "sale_price": 110000,
        "image": "images/products/u-shaped sofa.jpg",
        "description": (
            "Spacious U-shaped family sofa designed for large living rooms and "
            "comfortable family gatherings. Its generous seating arrangement "
            "provides plenty of room for family and guests while creating a "
            "beautiful centrepiece for the living room. Ideal for customers "
            "looking for a large, stylish and comfortable sofa for modern homes."
        ),
    },
    {
        "name": "Double Decker Bed",
        "slug": "double-decker-bed",
        "category": "Beds",
        "subcategory": "Bunk Beds",
        "price": 55000,
        "sale_price": 52000,
        "image": "images/products/bunk-bed.jpg",
        "description": (
            "Practical double-decker bunk bed designed to maximise sleeping "
            "space in shared bedrooms and children's rooms. Its stacked design "
            "makes efficient use of floor space while providing a practical "
            "sleeping solution for growing families."
        ),
    },
    {
        "name": "10 Seater Dining Set",
        "slug": "10-seater-dining-set",
        "category": "Dining Sets",
        "subcategory": "10 Seater",
        "price": 115000,
        "sale_price": 109000,
        "image": "images/products/dining10.jpg",
        "description": (
            "Spacious 10-seater dining set designed for large families and "
            "customers who regularly entertain guests. Its generous seating "
            "capacity makes it an excellent choice for large dining rooms, "
            "family meals and special occasions."
        ),
    },
    {
        "name": "Luxury Entertainment Unit",
        "slug": "luxury-entertainment-unit",
        "category": "TV Units",
        "subcategory": "Luxury",
        "price": 52000,
        "sale_price": 49000,
        "image": "images/products/tv-luxury.jpg",
        "description": (
            "Luxury entertainment unit designed to create an impressive and "
            "organised living-room entertainment area. Its stylish appearance "
            "provides an attractive focal point for your television and décor "
            "while complementing modern living-room furniture."
        ),
    },
]


def get_or_create_subcategory(category, name, slug, display_order):
    subcategory = Subcategory.query.filter_by(slug=slug).first()

    if not subcategory:
        subcategory = Subcategory(
            name=name,
            slug=slug,
            category_id=category.id,
            display_order=display_order,
            active=True,
        )
        db.session.add(subcategory)
        db.session.flush()

    return subcategory


with app.app_context():
    added = 0
    skipped = 0

    for item in products_to_add:
        existing = Product.query.filter_by(slug=item["slug"]).first()

        if existing:
            print(f"SKIPPED - already exists: {item['name']}")
            skipped += 1
            continue

        category = Category.query.filter_by(
            name=item["category"],
            active=True
        ).first()

        if not category:
            print(f"ERROR - category not found: {item['category']}")
            continue

        if item["subcategory"] == "U-Shaped":
            sub_slug = "sofas-u-shaped"
            order = 6
        elif item["subcategory"] == "Bunk Beds":
            sub_slug = "beds-bunk-beds"
            order = 9
        elif item["subcategory"] == "10 Seater":
            sub_slug = "dining-sets-10-seater"
            order = 4
        elif item["subcategory"] == "Luxury":
            sub_slug = "tv-units-luxury"
            order = 3
        else:
            sub_slug = item["subcategory"].lower().replace(" ", "-")
            order = 10

        subcategory = get_or_create_subcategory(
            category,
            item["subcategory"],
            sub_slug,
            order
        )

        product = Product(
            name=item["name"],
            slug=item["slug"],
            description=item["description"],
            price=item["price"],
            sale_price=item["sale_price"],
            image=item["image"],
            featured=True,
            best_seller=False,
            new_arrival=True,
            service_id=1,
            category_id=category.id,
            subcategory_id=subcategory.id,
        )

        db.session.add(product)
        added += 1
        print(f"ADDED - {item['name']}")

    db.session.commit()

    print()
    print("=" * 70)
    print(f"PRODUCTS ADDED: {added}")
    print(f"PRODUCTS SKIPPED: {skipped}")
    print(f"TOTAL PRODUCTS NOW: {Product.query.count()}")
    print("=" * 70)