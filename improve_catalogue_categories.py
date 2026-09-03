from app import create_app
from app.extensions import db
from app.models.category import Category
from app.models.subcategory import Subcategory

app = create_app()

subcategories = {
    "Sofas": [
        ("L-Shaped", "sofas-l-shaped"),
        ("U-Shaped", "sofas-u-shaped"),
        ("3 Seater", "sofas-3-seater"),
        ("5 Seater", "sofas-5-seater"),
        ("6 Seater", "sofas-6-seater"),
        ("7 Seater", "sofas-7-seater"),
        ("Recliner", "sofas-recliner"),
        ("Chesterfield", "sofas-chesterfield"),
        ("Modern", "sofas-modern"),
        ("Luxury", "sofas-luxury"),
    ],
    "Beds": [
        ("4x6 Beds", "beds-4x6"),
        ("Queen", "beds-queen"),
        ("King", "beds-king"),
        ("Bunk Beds", "beds-bunk-beds"),
        ("Storage Beds", "beds-storage"),
        ("Standard Beds", "beds-standard"),
    ],
    "Dining Sets": [
        ("4 Seater", "dining-sets-4-seater"),
        ("6 Seater", "dining-sets-6-seater"),
        ("8 Seater", "dining-sets-8-seater"),
        ("10 Seater", "dining-sets-10-seater"),
        ("Luxury Dining", "dining-sets-luxury-dining"),
    ],
    "TV Units": [
        ("Modern", "tv-units-modern"),
        ("Floating", "tv-units-floating"),
        ("Wall Mounted", "tv-units-wall-mounted"),
        ("Luxury", "tv-units-luxury"),
        ("Entertainment Units", "tv-units-entertainment-units"),
    ],
    "Wardrobes": [
        ("2 Door", "wardrobes-2-door"),
        ("3 Door", "wardrobes-3-door"),
        ("Sliding Door", "wardrobes-sliding-door"),
        ("Luxury", "wardrobes-luxury"),
    ],
    "Coffee Tables": [
        ("Modern", "coffee-tables-modern"),
        ("Luxury", "coffee-tables-luxury"),
        ("Marble", "coffee-tables-marble"),
    ],
}

with app.app_context():
    created = 0

    for category_name, items in subcategories.items():
        category = Category.query.filter_by(name=category_name).first()

        if not category:
            print(f"SKIPPED CATEGORY: {category_name}")
            continue

        for order, (name, slug) in enumerate(items, start=1):
            existing = Subcategory.query.filter_by(slug=slug).first()

            if existing:
                existing.name = name
                existing.category_id = category.id
                existing.active = True
                existing.display_order = order
            else:
                subcategory = Subcategory(
                    name=name,
                    slug=slug,
                    category_id=category.id,
                    active=True,
                    display_order=order,
                )
                db.session.add(subcategory)
                created += 1

    db.session.commit()

    print()
    print("=" * 70)
    print(f"NEW SUBCATEGORIES CREATED: {created}")
    print("=" * 70)