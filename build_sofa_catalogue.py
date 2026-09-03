from app import create_app
from app.extensions import db
from app.models.category import Category
from app.models.subcategory import Subcategory
from app.models.product import Product

app = create_app()

SOFA_SUBCATEGORIES = [
    ("L-Shaped Sofas", "sofas-l-shaped"),
    ("U-Shaped Sofas", "sofas-u-shaped"),
    ("Recliner Sofas", "sofas-recliner"),
    ("Chesterfield Sofas", "sofas-chesterfield"),
    ("Fabric Sofas", "sofas-fabric"),
    ("Leather Sofas", "sofas-leather"),
    ("Modern Sofas", "sofas-modern"),
    ("Luxury Sofas", "sofas-luxury"),
]

with app.app_context():

    sofas = Category.query.filter_by(name="Sofas").first()

    if not sofas:
        print("ERROR: Sofas category not found.")
        raise SystemExit(1)

    # Create the proper sofa collections
    subcategories = {}

    for order, (name, slug) in enumerate(SOFA_SUBCATEGORIES, start=1):

        subcategory = Subcategory.query.filter_by(slug=slug).first()

        if not subcategory:
            subcategory = Subcategory(
                name=name,
                slug=slug,
                category_id=sofas.id,
                active=True,
                display_order=order,
            )
            db.session.add(subcategory)
            print(f"CREATED SUBCATEGORY: {name}")
        else:
            subcategory.name = name
            subcategory.category_id = sofas.id
            subcategory.active = True
            subcategory.display_order = order
            print(f"EXISTS: {name}")

        subcategories[slug] = subcategory

    db.session.flush()

    # Put existing genuine sofa products into the correct collections
    product_mapping = {
        "6 Seater L-Shaped Sofa": "sofas-l-shaped",
        "U-Shaped Family Sofa": "sofas-u-shaped",
        "Recliner Sofa Set": "sofas-recliner",
        "3 Seater Chesterfield Sofa": "sofas-chesterfield",
        "5 Seater Modern Sofa": "sofas-modern",
        "7 Seater Luxury Sofa": "sofas-luxury",
    }

    print()
    print("=" * 70)
    print("REORGANIZING EXISTING SOFA PRODUCTS")
    print("=" * 70)

    updated = 0

    for product_name, subcategory_slug in product_mapping.items():

        product = Product.query.filter_by(name=product_name).first()

        if not product:
            print(f"NOT FOUND: {product_name}")
            continue

        product.category_id = sofas.id
        product.subcategory_id = subcategories[subcategory_slug].id

        updated += 1

        print(
            f"{product.name} -> "
            f"{subcategories[subcategory_slug].name}"
        )

    db.session.commit()

    print()
    print("=" * 70)
    print(f"SOFA PRODUCTS REORGANIZED: {updated}")
    print(f"SOFA COLLECTIONS CREATED/UPDATED: {len(SOFA_SUBCATEGORIES)}")
    print("=" * 70)

    print()
    print("CURRENT SOFA CATALOGUE")
    print("=" * 70)

    for slug, subcategory in subcategories.items():

        products = Product.query.filter_by(
            category_id=sofas.id,
            subcategory_id=subcategory.id
        ).order_by(Product.name.asc()).all()

        print()
        print(f"{subcategory.name}: {len(products)} product(s)")

        for product in products:
            price = product.sale_price or product.price
            print(f"  - {product.name} | KSh {price:,.0f}")