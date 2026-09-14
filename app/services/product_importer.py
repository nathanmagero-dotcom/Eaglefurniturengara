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
# These map the catalogue names to the EXACT existing
# database subcategory names.
#
# No duplicate categories or subcategories are created.
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
        "Queen Size Beds": "Queen",
        "King Size Beds": "King",
        "Standard": "Standard Beds",
        "Kids Beds": "Bunk Beds",
    },

    "Dining Sets": {
        "4-Seater Dining Sets": "4 Seater",
        "6-Seater Dining Sets": "6 Seater",
        "8-Seater Dining Sets": "8 Seater",
        "10-Seater Dining Sets": "10 Seater",
        "Luxury": "Luxury Dining",
    },

    "TV Units": {
        "Modern TV Units": "Modern",
        "Floating TV Units": "Floating",
        "Luxury TV Units": "Luxury",
        "Wall Mounted TV Units": "Wall Mounted",
    },

    "Coffee Tables": {
        "Modern Coffee Tables": "Modern",
        "Marble Coffee Tables": "Marble",
        "Luxury Coffee Tables": "Luxury",
    },

    "Wardrobes": {
        "2-Door Wardrobes": "2 Door",
        "3-Door Wardrobes": "3 Door",
        "Sliding Door Wardrobes": "Sliding Door",
        "Walk-In Wardrobes": "Bedroom",
    },

    "Office Furniture": {
        "Executive Desks": "Office Desk",
        "Office Chairs": "Office Chair",
    },

    "Mattresses": {
        "Orthopedic Mattresses": "Orthopedic",
        "Spring Mattresses": "Spring",
    },

    "Outdoor Furniture": {
        "Outdoor Patio Sets": "Patio",
        "Outdoor Swing Chairs": "Swing",
    },

    "Home Accessories": {
        "Wall Mirrors": "Mirror",
    },

    "Restaurant Furniture": {
        "Restaurant Tables": "Restaurant Tables",
        "Restaurant Chairs": "Restaurant Chairs",
        "RestaurantBooths": "Restaurant Booths",
        "Restaurant Booths": "Restaurant Booths",
        "Bar Furniture": "Bar Furniture",
        "Outdoor Restaurant Furniture": "Outdoor Restaurant Furniture",
    },

    "School Furniture": {
        "Student Desks": "Student Desks",
        "Student Chairs": "Student Chairs",
        "Teachers Desks": "Teachers Desks",
        "School Tables": "School Tables",
        "School Storage": "School Storage",
    },

    "Home Furniture": {
        "Wall Units": "Wall Units",
        "Console Tables": "Console Tables",
        "Side Tables": "Side Tables",
        "Benches": "Benches",
        "Home Storage": "Home Storage",
    },

    "Full Package Furniture": {
        "Living Room Package": "Living Room Package",
        "Bedroom Package": "Bedroom Package",
        "Dining Package": "Dining Package",
        "CompleteHome Package": "Complete Home Package",
        "Complete Home Package": "Complete Home Package",
        "OfficePackage": "Office Package",
        "Office Package": "Office Package",
    },
}


# ==========================================================
# SLUG HELPERS
# ==========================================================

def slugify(value):
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
        requested_name,
    )

    for item in category.subcategories:

        if (
            str(item.name).strip().lower()
            == resolved_name.lower()
        ):
            return item

    raise ValueError(
        f"Subcategory '{requested_name}' "
        f"resolved to '{resolved_name}', but "
        f"that subcategory was not found under "
        f"category '{category.name}'."
    )


# ==========================================================
# GALLERY HELPERS
# ==========================================================

def normalize_gallery(product_data):

    images = []

    main_image = product_data.get("image")

    if main_image:
        images.append(
            str(main_image).strip()
        )

    gallery_data = product_data.get(
        "gallery",
        [],
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
                    " ",
                ).title(),
                "value": str(value).strip(),
            }
        )

    return specifications


# ==========================================================
# PRODUCT LOOKUP
# ==========================================================

def find_existing_product(product_data):

    catalogue_id = product_data.get("id")

    if catalogue_id is not None:

        try:
            catalogue_id = int(catalogue_id)
        except (TypeError, ValueError):
            catalogue_id = None

    # ------------------------------------------------------
    # PRIMARY IDENTITY: DATABASE PRODUCT ID
    # ------------------------------------------------------

    if catalogue_id is not None:

        product = db.session.get(
            Product,
            catalogue_id,
        )

        if product is not None:
            return product

    # ------------------------------------------------------
    # FALLBACK IDENTITY: SKU
    #
    # Used only if an existing product cannot be found
    # by catalogue/database ID.
    # ------------------------------------------------------

    sku = product_data.get("sku")

    if sku:

        sku = str(
            sku
        ).strip().upper()

        product = Product.query.filter(
            Product.sku == sku
        ).first()

        if product is not None:
            return product

    return None


# ==========================================================
# VALIDATION
# ==========================================================

def validate_database_requirements():

    errors = []
    warnings = []

    seen_catalogue_ids = set()
    seen_skus = set()

    for product_data in products:

        name = str(
            product_data.get(
                "name",
                "Unnamed Product",
            )
        ).strip()

        catalogue_id = product_data.get("id")

        # --------------------------------------------------
        # ID
        # --------------------------------------------------

        if catalogue_id is None:

            errors.append(
                f"{name}: catalogue ID is missing."
            )

        else:

            try:
                catalogue_id = int(catalogue_id)
            except (TypeError, ValueError):

                errors.append(
                    f"{name}: catalogue ID must be numeric."
                )
                catalogue_id = None

            if catalogue_id is not None:

                if catalogue_id in seen_catalogue_ids:

                    errors.append(
                        f"{name}: duplicate catalogue ID "
                        f"{catalogue_id}."
                    )

                seen_catalogue_ids.add(catalogue_id)

        # --------------------------------------------------
        # NAME
        # --------------------------------------------------

        if not name:

            errors.append(
                f"Product {catalogue_id}: name is missing."
            )

        # --------------------------------------------------
        # PRICE
        # --------------------------------------------------

        price = None

        try:

            price = normalize_price(
                product_data.get("price"),
                "price",
                name,
            )

        except ValueError as exc:

            errors.append(str(exc))

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
                        f"{name}: sale price must be "
                        f"lower than regular price."
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
        # SKU
        #
        # Existing products do NOT require a SKU.
        # Only genuinely new database products require one.
        # --------------------------------------------------

        existing_product = find_existing_product(
            product_data
        )

        sku = product_data.get("sku")

        if existing_product is None:

            if not sku:

                errors.append(
                    f"{name}: SKU is required for a "
                    f"new product."
                )

            else:

                sku = str(
                    sku
                ).strip().upper()

                if sku in seen_skus:

                    errors.append(
                        f"{name}: duplicate SKU {sku}."
                    )

                seen_skus.add(sku)

        elif sku:

            sku = str(
                sku
            ).strip().upper()

            if sku in seen_skus:

                errors.append(
                    f"{name}: duplicate catalogue SKU {sku}."
                )

            seen_skus.add(sku)

        # --------------------------------------------------
        # IMAGE
        #
        # Missing images are warnings, NOT errors.
        # Existing database images/galleries are preserved.
        # --------------------------------------------------

        gallery = normalize_gallery(
            product_data
        )

        if not gallery:

            if existing_product is None:

                warnings.append(
                    f"{name}: no new image supplied; "
                    f"product will remain without a primary image."
                )

            elif not existing_product.image:

                warnings.append(
                    f"{name}: no verified image supplied "
                    f"and database product has no image."
                )

    return errors, warnings


# ==========================================================
# UPSERT PRODUCT
# ==========================================================

def upsert_product(product_data):

    name = str(
        product_data["name"]
    ).strip()

    product = find_existing_product(
        product_data
    )

    is_new = product is None

    # ------------------------------------------------------
    # Create genuinely new product
    # ------------------------------------------------------

    if is_new:

        sku = product_data.get("sku")

        if not sku:

            raise ValueError(
                f"{name}: SKU is required for a new product."
            )

        sku = str(
            sku
        ).strip().upper()

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
                f"{name}: sale price must be "
                f"lower than regular price."
            )

    # ------------------------------------------------------
    # Images
    #
    # IMPORTANT:
    # If the catalogue has a verified image/gallery,
    # update it.
    #
    # If it does not, preserve the existing database
    # image/gallery.
    # ------------------------------------------------------

    gallery = normalize_gallery(
        product_data
    )

    has_new_gallery = bool(gallery)

    # ------------------------------------------------------
    # Basic product data
    # ------------------------------------------------------

    product.name = name

    product.price = price

    product.sale_price = sale_price

    product.description = (
        product_data.get("description")
    )

    product.category = category

    product.subcategory = subcategory

    product.active = bool(
        product_data.get(
            "active",
            True,
        )
    )

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
    # DO NOT overwrite an existing SKU.
    #
    # Existing products may intentionally have no SKU.
    # Only genuinely new products receive the catalogue SKU.
    # ------------------------------------------------------

    if is_new and product_data.get("sku"):

        product.sku = str(
            product_data["sku"]
        ).strip().upper()

    # ------------------------------------------------------
    # Slug
    #
    # Existing slugs are preserved.
    # ------------------------------------------------------

    if not product.slug:

        product.slug = unique_product_slug(
            name,
            product.id,
        )

    # ------------------------------------------------------
    # SEO
    #
    # Fill missing SEO from catalogue first.
    # Otherwise use safe generated defaults.
    # ------------------------------------------------------

    catalogue_seo_title = product_data.get(
        "seo_title"
    )

    catalogue_seo_description = product_data.get(
        "seo_description"
    )

    if catalogue_seo_title:

        product.seo_title = str(
            catalogue_seo_title
        ).strip()

    elif not product.seo_title:

        product.seo_title = (
            f"{name} | Eagle Furniture Ngara"
        )

    if catalogue_seo_description:

        product.seo_description = str(
            catalogue_seo_description
        ).strip()

    elif not product.seo_description:

        product.seo_description = (
            f"Buy {name} from Eagle Furniture Ngara. "
            f"Custom-made furniture in Nairobi with "
            f"delivery available across Kenya."
        )

    # ------------------------------------------------------
    # Gallery records
    #
    # Only replace gallery when the catalogue actually
    # supplies verified images.
    # ------------------------------------------------------

    if has_new_gallery:

        product.image = gallery[0]

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
    # Specifications
    #
    # Only replace specifications when catalogue data
    # actually contains specifications.
    # ------------------------------------------------------

    specifications = build_specifications(
        product_data
    )

    if specifications:

        product.specifications.clear()

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
    # Add genuinely new product only after it is populated
    # ------------------------------------------------------

    if is_new:

        db.session.add(product)

    return product, is_new


# ==========================================================
# IMPORT CATALOGUE
# ==========================================================

def import_catalogue():

    print()
    print("=" * 65)
    print(
        "EAGLE FURNITURE NGARA - DATABASE IMPORTER"
    )
    print("=" * 65)
    print()

    print(
        "Running database compatibility validation..."
    )
    print()

    errors, warnings = (
        validate_database_requirements()
    )

    if errors:

        print("IMPORT CANCELLED")
        print("-" * 65)

        for error in errors:
            print(f"X {error}")

        print()

        print(
            f"{len(errors)} validation error(s) found."
        )

        return False

    print(
        "OK - Catalogue is compatible with the database."
    )

    if warnings:

        print()
        print(
            f"Warnings: {len(warnings)}"
        )

        for warning in warnings:
            print(f"  ! {warning}")

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
                    f"[ID {product.id}]"
                )

            else:

                updated += 1

                sku_display = (
                    product.sku
                    if product.sku
                    else "NO-SKU"
                )

                print(
                    f"  -> Updated: "
                    f"{product.name} "
                    f"[ID {product.id} | {sku_display}]"
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
            "IMPORT FAILED - DATABASE ROLLED BACK"
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

    print()
    print("=" * 65)
    print(
        "EAGLE FURNITURE NGARA - DATABASE IMPORT DRY RUN"
    )
    print("=" * 65)
    print()

    print(
        f"Catalogue products: {len(products)}"
    )

    print()

    errors, warnings = (
        validate_database_requirements()
    )

    if errors:

        print("DRY RUN FAILED")
        print("-" * 65)

        for error in errors:
            print(f"X {error}")

        print()

        print(
            f"{len(errors)} validation error(s) found."
        )

        if warnings:

            print()
            print(
                f"Warnings: {len(warnings)}"
            )

            for warning in warnings:
                print(f"  ! {warning}")

        print()

        return False

    print(
        "OK - All products match existing "
        "categories and subcategories."
    )

    print(
        "OK - Product IDs can be matched safely."
    )

    print(
        "OK - Prices are valid."
    )

    print(
        "OK - Missing images will not block import."
    )

    if warnings:

        print()
        print(
            f"Warnings: {len(warnings)}"
        )

        for warning in warnings:
            print(f"  ! {warning}")

    print()
    print(
        "OK - No database records were changed."
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
