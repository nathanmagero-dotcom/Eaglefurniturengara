from app import create_app
from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.subcategory import Subcategory

app = create_app()

with app.app_context():
    dining = Category.query.filter_by(name="Dining Sets").first()

    if not dining:
        print("ERROR: Dining Sets category not found.")
        raise SystemExit(1)

    mappings = {
        "4 Seater Dining Set": "dining-sets-4-seater",
        "6 Seater Dining Set": "dining-sets-6-seater",
        "8 Seater Dining Set": "dining-sets-8-seater",
        "10 Seater Dining Set": "dining-sets-10-seater",
    }

    for product_name, subcategory_slug in mappings.items():
        product = Product.query.filter_by(
            category_id=dining.id,
            name=product_name
        ).first()

        subcategory = Subcategory.query.filter_by(
            category_id=dining.id,
            slug=subcategory_slug
        ).first()

        if not product:
            print(f"ERROR: Product not found: {product_name}")
            continue

        if not subcategory:
            print(f"ERROR: Subcategory not found: {subcategory_slug}")
            continue

        product.subcategory = subcategory

        print(
            f"UPDATED: {product.name} -> {subcategory.name}"
        )

    db.session.commit()

    print("\nDining subcategories updated successfully.")