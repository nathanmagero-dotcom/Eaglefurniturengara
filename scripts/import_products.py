import sys
from pathlib import Path

# Make project root available to Python
sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parent.parent
    )
)

from app import create_app
from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.service import Service
from app.data.products import products
from slugify import slugify


app = create_app()


def find_category(category_name):
    """Find a category by name."""

    if not category_name:
        return None

    return (
        Category.query
        .filter(
            db.func.lower(Category.name)
            == category_name.strip().lower()
        )
        .first()
    )


def product_exists(name):
    """Check whether product already exists."""

    return (
        Product.query
        .filter(
            db.func.lower(Product.name)
            == name.strip().lower()
        )
        .first()
    )


with app.app_context():

    print("=" * 60)
    print("EAGLE FURNITURE NGARA")
    print("PRODUCT CATALOGUE IMPORT")
    print("=" * 60)

    # ---------------------------------------------------------
    # FURNITURE SERVICE
    # ---------------------------------------------------------

    furniture_service = (
        Service.query
        .filter(
            db.func.lower(Service.name) == "furniture"
        )
        .first()
    )

    if furniture_service is None:
        raise RuntimeError(
            "Furniture service was not found."
        )

    print(
        f"Service: {furniture_service.id} - "
        f"{furniture_service.name}"
    )

    print()

    # ---------------------------------------------------------
    # DATABASE CATEGORIES
    # ---------------------------------------------------------

    print("DATABASE CATEGORIES:")

    database_categories = {}

    for category in Category.query.all():

        database_categories[
            category.name.lower()
        ] = category

        print(
            f"  {category.id}: "
            f"{category.name}"
        )

    print()

    # ---------------------------------------------------------
    # CATEGORY MAPPINGS
    # ---------------------------------------------------------

    category_mappings = {
        "Home Accessories": "Home Furniture",
    }

    # ---------------------------------------------------------
    # CHECK CATALOGUE CATEGORIES
    # ---------------------------------------------------------

    catalogue_categories = sorted(
        set(
            item.get("category")
            for item in products
            if item.get("category")
        )
    )

    print("CATALOGUE CATEGORIES:")

    missing_categories = []

    for catalogue_category in catalogue_categories:

        mapped_category_name = category_mappings.get(
            catalogue_category,
            catalogue_category
        )

        category = database_categories.get(
            mapped_category_name.lower()
        )

        if category:

            if (
                catalogue_category
                != mapped_category_name
            ):

                print(
                    f"  MAPPED: "
                    f"{catalogue_category}"
                    f" -> "
                    f"{mapped_category_name}"
                )

            else:

                print(
                    f"  OK: "
                    f"{catalogue_category}"
                )

        else:

            print(
                f"  MISSING: "
                f"{catalogue_category}"
            )

            missing_categories.append(
                catalogue_category
            )

    print()

    # ---------------------------------------------------------
    # STOP IF CATEGORY IS STILL MISSING
    # ---------------------------------------------------------

    if missing_categories:

        print("=" * 60)
        print("IMPORT STOPPED")
        print("=" * 60)

        print(
            "The following catalogue categories "
            "do not exist in the database:"
        )

        for category_name in missing_categories:

            print(
                f"  - {category_name}"
            )

        print()

        raise SystemExit(1)

    # ---------------------------------------------------------
    # IMPORT PRODUCTS
    # ---------------------------------------------------------

    imported = 0
    skipped = 0

    print("=" * 60)
    print("IMPORTING PRODUCTS")
    print("=" * 60)

    for item in products:

        name = item.get("name")

        if not name:

            print(
                "SKIPPED: Product without name"
            )

            skipped += 1
            continue

        # -----------------------------------------------------
        # DUPLICATE CHECK
        # -----------------------------------------------------

        existing = product_exists(name)

        if existing:

            print(
                f"SKIPPED: {name}"
            )

            skipped += 1
            continue

        # -----------------------------------------------------
        # CATEGORY
        # -----------------------------------------------------

        catalogue_category = item.get(
            "category"
        )

        mapped_category_name = (
            category_mappings.get(
                catalogue_category,
                catalogue_category
            )
        )

        category = find_category(
            mapped_category_name
        )

        if category is None:

            print(
                f"SKIPPED: Category not found "
                f"for {name}"
            )

            skipped += 1
            continue

        # -----------------------------------------------------
        # SLUG
        # -----------------------------------------------------

        base_slug = slugify(name)

        slug = base_slug

        counter = 2

        while Product.query.filter_by(
            slug=slug
        ).first():

            slug = (
                f"{base_slug}-{counter}"
            )

            counter += 1

        # -----------------------------------------------------
        # CREATE PRODUCT
        # -----------------------------------------------------

        product = Product(

            name=name,

            slug=slug,

            description=item.get(
                "description"
            ),

            price=item.get(
                "price"
            ),

            sale_price=item.get(
                "sale_price"
            ),

            image=item.get(
                "image"
            ),

            featured=item.get(
                "featured",
                False
            ),

            best_seller=item.get(
                "best_seller",
                False
            ),

            new_arrival=item.get(
                "new_arrival",
                False
            ),

            service_id=furniture_service.id,

            category_id=category.id,
        )

        db.session.add(product)

        imported += 1

        print(
            f"IMPORTED: {name}"
        )

    # ---------------------------------------------------------
    # COMMIT
    # ---------------------------------------------------------

    db.session.commit()

    print()

    print("=" * 60)
    print("IMPORT COMPLETE")
    print("=" * 60)

    print(
        f"Imported: {imported}"
    )

    print(
        f"Skipped: {skipped}"
    )

    print(
        f"Database total: "
        f"{Product.query.count()}"
    )

    print("=" * 60)