from app import create_app
from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.subcategory import Subcategory

app = create_app()

with app.app_context():
    beds = Category.query.filter_by(name="Beds").first()

    if not beds:
        print("ERROR: Beds category not found.")
        raise SystemExit(1)

    bed_4x6 = Subcategory.query.filter_by(
        category_id=beds.id,
        slug="beds-4x6"
    ).first()

    product = Product.query.filter_by(
        category_id=beds.id,
        name="4x6 Bed"
    ).first()

    if not bed_4x6:
        print("ERROR: 4x6 Beds subcategory not found.")
        raise SystemExit(1)

    if not product:
        print("ERROR: 4x6 Bed product not found.")
        raise SystemExit(1)

    product.subcategory = bed_4x6
    db.session.commit()

    print("UPDATED:")
    print(f"Product: {product.name}")
    print(f"Subcategory: {product.subcategory.name}")
    print(f"Price: KSh {product.sale_price:,.0f}")