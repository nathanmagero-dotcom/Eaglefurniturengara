from app import create_app
from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.subcategory import Subcategory

app = create_app()

SOFA_PRODUCTS = {
    "6 Seater L-Shaped Sofa": "sofas-l-shaped",
    "5 Seater Modern Sofa": "sofas-modern",
    "7 Seater Luxury Sofa": "sofas-luxury",
    "3 Seater Chesterfield Sofa": "sofas-chesterfield",
    "7 Seater Recliner Sofa Set": "sofas-recliner",
    "Recliner Sofa Set": "sofas-recliner",
    "U-Shaped Family Sofa": "sofas-u-shaped",
}

with app.app_context():

    sofas = Category.query.filter_by(name="Sofas").first()

    if not sofas:
        raise SystemExit("ERROR: Sofas category not found.")

    updated = 0

    for product_name, subcategory_slug in SOFA_PRODUCTS.items():

        product = Product.query.filter_by(name=product_name).first()

        if not product:
            continue

        subcategory = Subcategory.query.filter_by(
            slug=subcategory_slug
        ).first()

        if not subcategory:
            print(f"SUBCATEGORY NOT FOUND: {subcategory_slug}")
            continue

        product.category_id = sofas.id
        product.subcategory_id = subcategory.id

        updated += 1

        price = product.sale_price or product.price

        print(
            f"UPDATED: {product.name} | "
            f"{subcategory.name} | "
            f"KSh {price:,.0f}"
        )

    db.session.commit()

    print()
    print("=" * 70)
    print(f"SOFA PRODUCTS UPDATED: {updated}")
    print("=" * 70)

    for subcategory in Subcategory.query.filter_by(
        category_id=sofas.id,
        active=True
    ).order_by(Subcategory.display_order).all():

        products = Product.query.filter_by(
            category_id=sofas.id,
            subcategory_id=subcategory.id
        ).order_by(Product.name).all()

        if products:
            print()
            print(f"{subcategory.name} ({len(products)})")

            for product in products:
                price = product.sale_price or product.price
                print(f"  {product.name} — KSh {price:,.0f}")