from app import create_app
from app.extensions import db
from app.models.product import Product

app = create_app()

image_updates = {
    "4x6 Bed": "images/products/bed.jpg",
    "Executive Office Desk": "images/products/office-desk.jpg",
    "Decorative Wall Mirror": "images/products/mirror.jpg",
}

with app.app_context():
    updated = 0

    for product_name, image_path in image_updates.items():
        product = Product.query.filter_by(name=product_name).first()

        if product:
            product.image = image_path
            updated += 1
            print(f"UPDATED: {product.name} -> {image_path}")
        else:
            print(f"NOT FOUND: {product_name}")

    db.session.commit()

    print()
    print("=" * 60)
    print(f"IMAGES UPDATED: {updated}")
    print("=" * 60)