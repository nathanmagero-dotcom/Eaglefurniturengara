import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.extensions import db
from app.models.category import Category
from app.models.subcategory import Subcategory
from app.models.product import Product
from app.data.products import products as product_data


app = create_app()


def slugify(value):
    return (
        value.strip()
        .lower()
        .replace("&", "and")
        .replace("/", "-")
        .replace(" ", "-")
    )


with app.app_context():

    print("\n========================================")
    print("EAGLE FURNITURE")
    print("SUBCATEGORY SEED")
    print("========================================\n")

    created = 0
    existing = 0
    linked = 0
    skipped = 0

    # ----------------------------------------------------------
    # CREATE SUBCATEGORIES
    # ----------------------------------------------------------

    subcategory_cache = {}

    for product_data_item in product_data:

        category_name = product_data_item.get("category")
        subcategory_name = product_data_item.get("subcategory")

        if not category_name or not subcategory_name:
            skipped += 1
            continue

        category = Category.query.filter_by(
            name=category_name
        ).first()

        if not category:
            print(
                f"WARNING: Category not found: {category_name}"
            )
            skipped += 1
            continue

        cache_key = (
            category.id,
            subcategory_name.lower()
        )

        if cache_key in subcategory_cache:
            subcategory = subcategory_cache[cache_key]

        else:

            subcategory = Subcategory.query.filter_by(
                category_id=category.id,
                name=subcategory_name
            ).first()

            if subcategory:

                existing += 1

            else:

                subcategory = Subcategory(
                    category_id=category.id,
                    name=subcategory_name,
                    slug=slugify(
                        f"{category.slug}-{subcategory_name}"
                    ),
                    description=(
                        f"{subcategory_name} "
                        f"{category.name} furniture."
                    ),
                    icon=None,
                    image=None,
                    active=True,
                    display_order=0
                )

                db.session.add(subcategory)

                created += 1

                print(
                    f"CREATED: "
                    f"{category.name} → "
                    f"{subcategory_name}"
                )

            subcategory_cache[cache_key] = subcategory

    db.session.flush()

    # ----------------------------------------------------------
    # LINK EXISTING DATABASE PRODUCTS
    # ----------------------------------------------------------

    for product_data_item in product_data:

        product_name = product_data_item.get("name")
        category_name = product_data_item.get("category")
        subcategory_name = product_data_item.get("subcategory")

        if not product_name or not subcategory_name:
            continue

        product = Product.query.filter_by(
            name=product_name
        ).first()

        if not product:

            print(
                f"WARNING: Product not found: "
                f"{product_name}"
            )

            skipped += 1
            continue

        category = Category.query.filter_by(
            name=category_name
        ).first()

        if not category:
            skipped += 1
            continue

        subcategory = Subcategory.query.filter_by(
            category_id=category.id,
            name=subcategory_name
        ).first()

        if not subcategory:
            skipped += 1
            continue

        if product.subcategory_id != subcategory.id:

            product.subcategory_id = subcategory.id

            linked += 1

            print(
                f"LINKED: "
                f"{product.name} → "
                f"{subcategory.name}"
            )

    # ----------------------------------------------------------
    # SAVE
    # ----------------------------------------------------------

    db.session.commit()

    print("\n========================================")
    print("SEED COMPLETE")
    print("========================================")
    print(f"Created subcategories : {created}")
    print(f"Existing subcategories: {existing}")
    print(f"Products linked       : {linked}")
    print(f"Skipped               : {skipped}")
    print(
        f"Total subcategories   : "
        f"{Subcategory.query.count()}"
    )
    print(
        f"Total products        : "
        f"{Product.query.count()}"
    )
    print("========================================\n")