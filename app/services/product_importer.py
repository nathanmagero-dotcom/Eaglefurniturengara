from __future__ import annotations

import re
import sys
import unicodedata
from decimal import Decimal, InvalidOperation

from app import create_app
from app.extensions import db
from app.models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
)
from app.data.products import products


# ==========================================================
# CONFIGURATION
# ==========================================================

SPECIFICATION_FIELDS = (
    "material",
    "fabric",
    "colour",
    "size",
    "stock",
    "delivery",
    "warranty",
    "rating",
    "reviews",
)


# ==========================================================
# SUBCATEGORY ALIASES
# ==========================================================
#
# The catalogue uses shorter names while the database already
# contains the correct, richer collection names.
#
# We map catalogue names to existing database records.
#
# We DO NOT create duplicate subcategories.
# ==========================================================

SUBCATEGORY_ALIASES = {
    "Sofas": {
        "L-Shaped": "L-Shaped Sofas",
        "Modern": "Modern Sofas",
        "Luxury": "Luxury Sofas",
        "Chesterfield": "Chesterfield Sofas",
        "Recliner": "Recliner Sofas",
    },

    "Beds": {
        "Standard": "Standard Beds",
        "Kids": "Bunk Beds",
    },

    "Dining Sets": {
        "Luxury": "Luxury Dining",
    },
}


# ==========================================================
# SLUG HELPERS
# ==========================================================

def slugify(value):
    """
    Convert a value into a clean URL slug.
    """

    value = unicodedata.normalize(
        "NFKD",
        str(value),
    )

    value = value.encode(
        "ascii",
        "ignore",
    ).decode("ascii")

    value = value.lower()

    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        value,
    )

    value = re.sub(
        r"-+",
        "-",
        value,
    )

    return value.strip("-")


def unique_product_slug(name, product_id=None):
    """
    Generate a unique product slug.

    Existing product slugs are preserved during updates.
    """

    base_slug = slugify(name)

    if not base_slug:
        raise ValueError(
            f"Unable to generate slug for product: {name}"
        )

    slug = base_slug
    counter = 2

    while True:

        query = Product.query.filter(
            Product.slug == slug
        )

        if product_id is not None:
            query = query.filter(
                Product.id != product_id
            )

        existing = query.first()

        if existing is None:
            return slug

        slug = f"{base_slug}-{counter}"
        counter += 1


# ==========================================================
# PRICE HELPERS
# ==========================================================

def normalize_price(value, field_name, product_name):
    """
    Validate and normalize a price.
    """

    if value is None:
        raise ValueError(
            f"{product_name}: {field_name} is missing."
        )

    if isinstance(value, bool):
        raise ValueError(
            f"{product_name}: {field_name} cannot be boolean."
        )

    try:
        value = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(
            f"{product_name}: {field_name} must be numeric."
        )

    if value < 0:
        raise ValueError(
            f"{product_name}: {field_name} cannot be negative."
        )

    if value != value.to_integral_value():
        raise ValueError(
            f"{product_name}: {field_name} must be a whole number."
        )

    return int(value)


# ==========================================================
# CATEGORY HELPERS
# ==========================================================

def get_category(category_name):
    """
    Find an existing category.

    Categories are never automatically created.
    """

    if not category_name:
        raise ValueError(
            "Category name is missing."
        )

    category = Category.query.filter(
        db.func.lower(Category.name)
        == str(category_name).strip().lower()
    ).first()

    if category is None:
        raise ValueError(
            f"Category not found: {category_name}"
        )

    return category


def get_subcategory(category, subcategory_name):
    """
    Find an existing subcategory belonging to
    the correct category.

    Catalogue aliases are mapped to the existing
    database structure.
    """

    if not subcategory_name:
        raise ValueError(
            f"Subcategory is missing under "
            f"category '{category.name}'."
        )

    requested_name = str(
        subcategory_name
    ).strip()

    category_aliases = SUBCATEGORY_ALIASES.get(
        category.name,
        {}
    )

    resolved_name = category_aliases.get(
        requested_name,
        requested_name
    )

    for item in category.subcategories:

        if (
            str(item.name).strip().lower()
            == resolved_name.lower()
        ):
            return item

    if resolved_name != requested_name:

        raise ValueError(
            f"Subcategory '{requested_name}' "
            f"maps to '{resolved_name}', but "
            f"'{resolved_name}' was not found under "
            f"category '{category.name}'."
        )

    raise ValueError(
        f"Subcategory '{requested_name}' "
        f"not found under category "
        f"'{category.name}'."
    )


# ==========================================================
# GALLERY NORMALIZATION
# ==========================================================

def normalize_gallery(product_data):
    """
    Build a clean product gallery.

    Rules:
    - Main image comes first.
    - Empty values are removed.
    - Duplicate images are removed.
    - Original order is preserved.
    """

    images = []

    main_image = product_data.get("image")

    if main_image:
        images.append(
            str(main_image).strip()
        )

    gallery_data = product_data.get(
        "gallery",
        []
    )

    if gallery_data is None:
        gallery_data = []

    for image in gallery_data:

        if image:
            images.append(
                str(image).strip()
            )

    cleaned = []

    for image in images:

        if image and image not in cleaned:
            cleaned.append(image)

    return cleaned


# ==========================================================
# SPECIFICATION HELPERS
# ==========================================================

def build_specifications(product_data):
    """
    Convert catalogue fields into
    ProductSpecification records.
    """

    specifications = []

    for field in SPECIFICATION_FIELDS:

        value = product_data.get(field)

        if value is None:
            continue

        if str(value).strip() == "":
            continue

        specifications.append(
            {
                "name": field.replace(
                    "_",
                    " "
                ).title(),
                "value": str(value).strip(),
            }
        )

    return specifications


# ==========================================================
# PRODUCT VALIDATION
# ==========================================================

def validate_database_requirements():
    """
    Validate the complete catalogue against
    the current database.

    No database writes happen here.
    """

    errors = []

    seen_skus = set()

    for product_data in products:

        name = product_data.get(
            "name",
            "Unnamed Product",
        )

        # --------------------------------------------------
        # SKU
        # --------------------------------------------------

        sku = product_data.get("sku")

        if not sku:
            errors.append(
                f"{name}: SKU is missing."
            )
            continue

        sku = str(
            sku
        ).strip().upper()

        if sku in seen_skus:

            errors.append(
                f"{name}: duplicate SKU {sku}."
            )

        seen_skus.add(sku)

        # --------------------------------------------------
        # NAME
        # --------------------------------------------------

        if not str(name).strip():

            errors.append(
                f"Product with SKU {sku}: "
                f"name is missing."
            )

        # --------------------------------------------------
        # PRICE
        # --------------------------------------------------

        try:

            price = normalize_price(
                product_data.get("price"),
                "price",
                name,
            )

        except ValueError as exc:

            errors.append(str(exc))
            price = None

        # --------------------------------------------------
        # SALE PRICE
        # --------------------------------------------------

        sale_price_value = product_data.get(
            "sale_price"
        )

        if sale_price_value is not None:

            try:

                sale_price = normalize_price(
                    sale_price_value,
                    "sale_price",
                    name,
                )

                if (
                    price is not None
                    and sale_price >= price
                ):

                    errors.append(
                        f"{name}: sale price "
                        f"must be lower than "
                        f"regular price."
                    )

            except ValueError as exc:

                errors.append(str(exc))

        # --------------------------------------------------
        # CATEGORY
        # --------------------------------------------------

        try:

            category = get_category(
                product_data.get("category")
            )

        except ValueError as exc:

            errors.append(str(exc))
            continue

        # --------------------------------------------------
        # SUBCATEGORY
        # --------------------------------------------------

        try:

            get_subcategory(
                category,
                product_data.get(
                    "subcategory"
                ),
            )

        except ValueError as exc:

            errors.append(str(exc))

        # --------------------------------------------------
        # IMAGE
        # --------------------------------------------------

        gallery = normalize_gallery(
            product_data
        )

        if not gallery:

            errors.append(
                f"{name}: no product images found."
            )

    return errors


# ==========================================================
# UPSERT PRODUCT
# ==========================================================

def upsert_product(product_data):
    """
    Insert or update one product.

    SKU is the permanent catalogue identity.

    Important:
    A new Product is NOT added to the SQLAlchemy session
    until all required Product fields have been populated.
    This prevents premature autoflush errors.
    """

    sku = str(
        product_data["sku"]
    ).strip().upper()

    name = str(
        product_data["name"]
    ).strip()

    # ------------------------------------------------------
    # Find existing product
    # ------------------------------------------------------

    product = Product.query.filter(
        Product.sku == sku
    ).first()

    is_new = product is None

    if is_new:

        # Create an uncommitted object.
        #
        # DO NOT call db.session.add(product) here.
        #
        # The object will be added only after all required
        # fields have been populated.
        product = Product(
            sku=sku
        )

    # ------------------------------------------------------
    # Category
    # ------------------------------------------------------

    category = get_category(
        product_data["category"]
    )

    subcategory = get_subcategory(
        category,
        product_data["subcategory"],
    )

    # ------------------------------------------------------
    # Prices
    # ------------------------------------------------------

    price = normalize_price(
        product_data["price"],
        "price",
        name,
    )

    sale_price = None

    if product_data.get("sale_price") is not None:

        sale_price = normalize_price(
            product_data["sale_price"],
            "sale_price",
            name,
        )

        if sale_price >= price:

            raise ValueError(
                f"{name}: sale price "
                f"must be lower than "
                f"regular price."
            )

    # ------------------------------------------------------
    # Gallery
    # ------------------------------------------------------

    gallery = normalize_gallery(
        product_data
    )

    if not gallery:

        raise ValueError(
            f"{name}: no product images found."
        )

    # ------------------------------------------------------
    # Basic product data
    # ------------------------------------------------------

    product.name = name

    product.price = price

    product.sale_price = sale_price

    product.description = (
        product_data.get("description")
    )

    product.image = gallery[0]

    product.category = category

    product.subcategory = subcategory

    product.active = True

    product.featured = bool(
        product_data.get(
            "featured",
            False,
        )
    )

    product.best_seller = bool(
        product_data.get(
            "best_seller",
            False,
        )
    )

    product.new_arrival = bool(
        product_data.get(
            "new_arrival",
            False,
        )
    )

    # ------------------------------------------------------
    # Slug
    # ------------------------------------------------------

    if not product.slug:

        product.slug = unique_product_slug(
            name,
            product.id,
        )

    # ------------------------------------------------------
    # SEO
    # ------------------------------------------------------

    if not product.seo_title:

        product.seo_title = (
            f"{name} | Eagle Furniture Ngara"
        )

    if not product.seo_description:

        product.seo_description = (
            f"Buy {name} from Eagle Furniture Ngara. "
            f"Custom-made furniture in Nairobi with "
            f"delivery available."
        )

    # ------------------------------------------------------
    # Gallery records
    # ------------------------------------------------------

    product.gallery.clear()

    for index, image in enumerate(gallery):

        gallery_image = ProductImage(
            image=image,
            alt_text=name,
            display_order=index,
            is_primary=(index == 0),
        )

        product.gallery.append(
            gallery_image
        )

    # ------------------------------------------------------
    # Specification records
    # ------------------------------------------------------

    product.specifications.clear()

    specifications = build_specifications(
        product_data
    )

    for index, specification in enumerate(
        specifications
    ):

        product_specification = ProductSpecification(
            name=specification["name"],
            value=specification["value"],
            display_order=index,
        )

        product.specifications.append(
            product_specification
        )

    # ------------------------------------------------------
    # Add NEW product only after it is fully populated
    # ------------------------------------------------------

    if is_new:
        db.session.add(product)

    return product, is_new


# ==========================================================
# IMPORT CATALOGUE
# ==========================================================

def import_catalogue():
    """
    Import the complete catalogue into the database.

    The entire operation is transactional.

    If any product fails, the entire transaction
    is rolled back.
    """

    print()
    print("=" * 65)
    print(
        "EAGLE FURNITURE NGARA — DATABASE IMPORTER"
    )
    print("=" * 65)
    print()

    # ------------------------------------------------------
    # Validate first
    # ------------------------------------------------------

    print(
        "Running database compatibility validation..."
    )

    print()

    errors = validate_database_requirements()

    if errors:

        print("IMPORT CANCELLED")
        print("-" * 65)

        for error in errors:
            print(f"✗ {error}")

        print()

        print(
            f"{len(errors)} validation error(s) found."
        )

        return False

    print(
        "✓ Catalogue is compatible with the database."
    )

    print()

    created = 0
    updated = 0

    try:

        for product_data in products:

            product, is_new = upsert_product(
                product_data
            )

            if is_new:

                created += 1

                print(
                    f"  + Created: "
                    f"{product.name} "
                    f"[{product.sku}]"
                )

            else:

                updated += 1

                print(
                    f"  ↻ Updated: "
                    f"{product.name} "
                    f"[{product.sku}]"
                )

        # --------------------------------------------------
        # Commit EVERYTHING only after all products succeed
        # --------------------------------------------------

        db.session.commit()

    except Exception as exc:

        db.session.rollback()

        print()
        print("=" * 65)
        print(
            "IMPORT FAILED — DATABASE ROLLED BACK"
        )
        print("=" * 65)
        print()

        print(str(exc))

        return False

    print()
    print("=" * 65)
    print(
        "IMPORT COMPLETED SUCCESSFULLY"
    )
    print("=" * 65)
    print()

    print(
        f"Products created : {created}"
    )

    print(
        f"Products updated : {updated}"
    )

    print(
        f"Products total   : {created + updated}"
    )

    print()

    return True


# ==========================================================
# DRY RUN
# ==========================================================

def dry_run():
    """
    Validate the catalogue against the database
    without changing database records.
    """

    print()
    print("=" * 65)
    print(
        "EAGLE FURNITURE NGARA — DATABASE IMPORT DRY RUN"
    )
    print("=" * 65)
    print()

    print(
        f"Catalogue products: {len(products)}"
    )

    print()

    errors = validate_database_requirements()

    if errors:

        print("DRY RUN FAILED")
        print("-" * 65)

        for error in errors:
            print(f"✗ {error}")

        print()

        return False

    print(
        "✓ All products match existing "
        "categories and subcategories."
    )

    print(
        "✓ Prices are valid."
    )

    print(
        "✓ Gallery data is valid."
    )

    print(
        "✓ No database records were changed."
    )

    print()
    print("=" * 65)
    print("DRY RUN PASSED")
    print("=" * 65)
    print()

    return True


# ==========================================================
# COMMAND LINE
# ==========================================================

def main():

    app = create_app()

    with app.app_context():

        command = (
            sys.argv[1]
            if len(sys.argv) > 1
            else "dry-run"
        )

        if command == "dry-run":

            success = dry_run()

        elif command == "import":

            success = import_catalogue()

        else:

            print(
                "Unknown command."
            )

            print()

            print(
                "Use:"
            )

            print(
                "  python -m "
                "app.services.product_importer dry-run"
            )

            print(
                "  python -m "
                "app.services.product_importer import"
            )

            success = False

        raise SystemExit(
            0 if success else 1
        )


if __name__ == "__main__":
    main()