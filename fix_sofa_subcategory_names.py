from app import create_app, db
from app.models.category import Category
from app.models.subcategory import Subcategory

app = create_app()

with app.app_context():

    category = Category.query.filter_by(name="Sofas").first()

    if not category:
        raise RuntimeError("Sofas category not found.")

    fixes = {
        "ModernSofas": "Modern Sofas",
        "LuxurySofas": "Luxury Sofas",
    }

    for old_name, new_name in fixes.items():

        subcategory = Subcategory.query.filter_by(
            category_id=category.id,
            name=old_name
        ).first()

        if subcategory:
            existing = Subcategory.query.filter_by(
                category_id=category.id,
                name=new_name
            ).first()

            if existing and existing.id != subcategory.id:
                print(f"SKIP: {new_name} already exists.")
                continue

            subcategory.name = new_name
            subcategory.slug = new_name.lower().replace(" ", "-")
            db.session.commit()

            print(f"FIXED: {old_name} -> {new_name}")

        else:
            print(f"NOT FOUND: {old_name}")

    print("\nCURRENT SOFA SUBCATEGORIES")
    print("=" * 60)

    subcategories = (
        Subcategory.query
        .filter_by(category_id=category.id)
        .order_by(Subcategory.display_order, Subcategory.name)
        .all()
    )

    for sub in subcategories:
        count = len(sub.products)
        print(f"{sub.name} | {count} product(s) | {sub.slug}")