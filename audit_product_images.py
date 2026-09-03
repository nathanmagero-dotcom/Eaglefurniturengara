from app import create_app
from app.models.product import Product
import os

app = create_app()

IMAGE_DIR = os.path.join(
    app.root_path,
    "static",
    "images",
    "products"
)

with app.app_context():
    products = Product.query.order_by(Product.id.asc()).all()

    print()
    print("=" * 80)
    print("EAGLE FURNITURE NGARA - PRODUCT IMAGE AUDIT")
    print("=" * 80)

    with_images = 0
    missing_images = 0
    broken_images = 0

    for product in products:
        if not product.image:
            status = "MISSING"
            missing_images += 1

        else:
            filename = os.path.basename(product.image)
            full_path = os.path.join(IMAGE_DIR, filename)

            if os.path.exists(full_path):
                status = "OK"
                with_images += 1
            else:
                status = "BROKEN PATH"
                broken_images += 1

        print(
            f"{product.id:02d} | "
            f"{status:11} | "
            f"{product.name} | "
            f"{product.image or '-'}"
        )

    print()
    print("=" * 80)
    print(f"TOTAL PRODUCTS : {len(products)}")
    print(f"WITH IMAGES    : {with_images}")
    print(f"MISSING IMAGES : {missing_images}")
    print(f"BROKEN PATHS   : {broken_images}")
    print("=" * 80)