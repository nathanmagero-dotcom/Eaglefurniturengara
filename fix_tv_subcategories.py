from app import create_app
from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.subcategory import Subcategory

app = create_app()

with app.app_context():
    tv = Category.query.filter_by(name="TV Units").first()

    if not tv:
        print("ERROR: TV Units category not found.")
        raise SystemExit(1)

    mappings = {
        "Floating TV Unit": "tv-units-floating",
        "Luxury Entertainment Unit": "tv-units-entertainment-units",
    }

    for product_name, subcategory_slug in mappings.items():
        product = Product.query.filter_by(
            category_id=tv.id,
            name=product_name
        ).first()

        subcategory = Subcategory.query.filter_by(
            category_id=tv.id,
            slug=subcategory_slug
        ).first()

        if not product:
            print(f"ERROR: Product not found: {product_name}")
            continue

        if not subcategory:
            print(f"ERROR: Subcategory not found: {subcategory_slug}")
            continue

        product.subcategory = subcategory
        print(f"UPDATED: {product.name} -> {subcategory.name}")

    db.session.commit()

    print("\nTV subcategories updated successfully.")