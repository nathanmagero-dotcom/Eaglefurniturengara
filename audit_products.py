from app import create_app
from app.models.product import Product

app = create_app()

with app.app_context():
    products = Product.query.order_by(Product.id).all()

    print("=" * 100)
    print(f"TOTAL PRODUCTS: {len(products)}")
    print("=" * 100)

    for p in products:
        category = p.category.name if p.category else "NO CATEGORY"
        subcategory = p.subcategory.name if p.subcategory else "NO SUBCATEGORY"
        description = "YES" if p.description else "NO"
        image = p.image if p.image else "NO IMAGE"

        print(
            f"{p.id} | "
            f"{p.name} | "
            f"{category} | "
            f"{subcategory} | "
            f"KSh {p.price} | "
            f"Sale: {p.sale_price} | "
            f"Image: {image} | "
            f"Featured: {p.featured} | "
            f"Best: {p.best_seller} | "
            f"New: {p.new_arrival} | "
            f"Description: {description} | "
            f"Service: {p.service_id}"
        )