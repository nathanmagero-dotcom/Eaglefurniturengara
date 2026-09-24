from app import create_app
from app.models.product import Product
import os

app = create_app()

with app.app_context():
    products = Product.query.order_by(Product.id).all()

    print("=" * 120)
    print(f"TOTAL PRODUCTS: {len(products)}")
    print("=" * 120)

    static_root = app.static_folder

    for p in products:
        category = p.category.name if p.category else "NO CATEGORY"
        subcategory = p.subcategory.name if p.subcategory else "NO SUBCATEGORY"

        description = "YES" if p.description else "NO"
        image = p.image if p.image else "NO IMAGE"

        image_exists = (
            "YES"
            if p.image and os.path.isfile(os.path.join(static_root, p.image))
            else "NO"
        )

        gallery_count = len(p.gallery) if p.gallery else 0
        specification_count = len(p.specifications) if p.specifications else 0

        print(
            f"{p.id} | "
            f"{p.name} | "
            f"Slug: {p.slug} | "
            f"Category: {category} | "
            f"Subcategory: {subcategory} | "
            f"Price: KSh {p.price} | "
            f"Sale: KSh {p.sale_price} | "
            f"Active: {p.active} | "
            f"Image: {image} | "
            f"Image Exists: {image_exists} | "
            f"Gallery: {gallery_count} | "
            f"Specs: {specification_count} | "
            f"Featured: {p.featured} | "
            f"Best: {p.best_seller} | "
            f"New: {p.new_arrival} | "
            f"Description: {description} | "
            f"SKU: {p.sku or 'NO SKU'}"
        )