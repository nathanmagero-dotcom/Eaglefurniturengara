from pathlib import Path
import shutil
import sys
import re
from datetime import datetime

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.extensions import db
from app.models.product import Product
from app.models.category import Category


# ============================================================
# APP
# ============================================================

app = create_app()

STATIC_ROOT = Path(app.static_folder)

PRODUCTS_DIR = STATIC_ROOT / "images" / "products"
CATEGORIES_DIR = STATIC_ROOT / "images" / "categories"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
}


# ============================================================
# SAFE IMAGE MAP
# ============================================================

SAFE_PRODUCT_IMAGES = {

    # SOFAS
    "6 Seater L-Shaped Sofa":
        "images/products/lshape1.jpg",

    "5 Seater Modern Sofa":
        "images/products/sofa2.jpg",

    "7 Seater Luxury Sofa":
        "images/products/luxury1.jpg",

    "Recliner Sofa Set":
        "images/products/recliner.jpg",


    # BEDS
    "Queen Size Bed":
        "images/products/bed.jpg",

    "King Size Bed":
        "images/products/bed.jpg",

    "4x6 Bed":
        "images/products/bed.jpg",


    # DINING
    "4 Seater Dining Set":
        "images/products/dining-set.jpg",

    "6 Seater Dining Set":
        "images/products/dining-set.jpg",

    "8 Seater Dining Set":
        "images/products/dining-set.jpg",


    # TV
    "Modern TV Unit":
        "images/products/tv-unit.jpg",

    "Floating TV Unit":
        "images/products/tv-unit.jpg",


    # COFFEE TABLES
    "Modern Coffee Table":
        "images/products/coffee-table.jpg",

    "Luxury Marble Coffee Table":
        "images/products/coffee-table.jpg",


    # WARDROBE
    "2 Door Wardrobe":
        "images/products/wardrobe2.jpg",
}


# ============================================================
# PRODUCTS THAT MUST NOT USE GENERIC IMAGES
# ============================================================

NO_SAFE_IMAGE_PRODUCTS = {
    "3 Seater Chesterfield Sofa",

    "3 Door Wardrobe",
    "Sliding Door Wardrobe",

    "Executive Office Desk",
    "Ergonomic Office Chair",

    "6x6 Orthopedic Mattress",
    "5x6 Spring Mattress",

    "Outdoor Patio Set",
    "Outdoor Swing Chair",

    "Decorative Wall Mirror",

    "Commercial Restaurant Chairs",
    "Custom Restaurant Booth Seating",
    "Commercial Bar Stools",

    "Two-Seater Student Desk",
    "School Student Chair",
    "Teachers Office Desk",
    "Classroom Tables",
    "School Storage Cabinet",

    "Modern Home Wall Unit",
    "Modern Console Table",
    "Wooden Side Table",
    "Custom Wooden Bench",
    "Home Storage Cabinet",

    "Living Room Furniture Package",
    "Bedroom Furniture Package",
    "Complete Home Furniture Package",
    "Complete Office Furniture Package",

    "Outdoor Restaurant Dining Set",
    "Custom Restaurant Dining Table",
}


# ============================================================
# CATEGORY IMAGE MAP
# ============================================================

SAFE_CATEGORY_IMAGES = {
    # Add category images here when they actually exist.
    #
    # Example:
    #
    # "Beds": "images/categories/beds.jpg",
    #
}


# ============================================================
# HELPERS
# ============================================================

def normalize(value):
    if not value:
        return ""

    value = str(value).lower()

    value = re.sub(
        r"[^a-z0-9]+",
        " ",
        value,
    )

    return " ".join(value.split())


def image_exists(relative_path):
    if not relative_path:
        return False

    path = STATIC_ROOT / relative_path.replace("/", "\\")

    return path.is_file()


def get_images(directory):
    if not directory.exists():
        return []

    return [
        path
        for path in directory.rglob("*")
        if path.is_file()
        and path.suffix.lower() in IMAGE_EXTENSIONS
    ]


def database_path_exists(relative_path):
    return image_exists(relative_path)


# ============================================================
# DATABASE BACKUP
# ============================================================

def backup_database():

    db_uri = app.config.get(
        "SQLALCHEMY_DATABASE_URI",
        "",
    )

    if not db_uri.startswith("sqlite:///"):
        print("[WARNING] Database is not SQLite.")
        return None

    db_path = db_uri.replace(
        "sqlite:///",
        "",
        1,
    )

    db_file = Path(db_path)

    if not db_file.is_absolute():
        db_file = PROJECT_ROOT / db_file

    if not db_file.exists():
        print(
            "[WARNING] Database file not found:"
        )
        print(
            f"          {db_file}"
        )
        return None

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup = db_file.with_name(
        f"{db_file.stem}_before_image_repair_{timestamp}"
        f"{db_file.suffix}"
    )

    shutil.copy2(
        db_file,
        backup,
    )

    print(
        f"[BACKUP] {backup}"
    )

    return backup


# ============================================================
# PRODUCT IMAGE REPAIR
# ============================================================

def repair_products():

    print()
    print("=" * 70)
    print("PRODUCT IMAGE CHECK")
    print("=" * 70)

    available_images = get_images(
        PRODUCTS_DIR
    )

    available_relative = {
        p.relative_to(STATIC_ROOT).as_posix()
        for p in available_images
    }

    repaired = 0
    valid = 0
    cleared = 0
    missing = 0

    products = (
        Product.query
        .order_by(Product.id.asc())
        .all()
    )

    for product in products:

        name = product.name.strip()

        # ----------------------------------------------------
        # 1. Existing valid image
        # ----------------------------------------------------

        if database_path_exists(product.image):

            # Special protection against previously
            # incorrect automatic assignments.
            if name in NO_SAFE_IMAGE_PRODUCTS:

                print()
                print(
                    f"[CLEAR]   Product {product.id}: {name}"
                )
                print(
                    f"          OLD: {product.image}"
                )
                print(
                    "          Reason: no safe image exists."
                )

                product.image = None

                cleared += 1

                continue

            print(
                f"[OK]      Product {product.id}: "
                f"{name} -> {product.image}"
            )

            valid += 1

            continue

        # ----------------------------------------------------
        # 2. Known safe mapping
        # ----------------------------------------------------

        mapped_image = SAFE_PRODUCT_IMAGES.get(
            name
        )

        if mapped_image:

            if mapped_image in available_relative:

                old_path = product.image

                product.image = mapped_image

                print()
                print(
                    f"[AUTO]    Product {product.id}: {name}"
                )
                print(
                    f"          OLD: {old_path}"
                )
                print(
                    f"          NEW: {mapped_image}"
                )

                repaired += 1

                continue

        # ----------------------------------------------------
        # 3. Explicitly unsafe product
        # ----------------------------------------------------

        if name in NO_SAFE_IMAGE_PRODUCTS:

            if product.image:

                print()
                print(
                    f"[CLEAR]   Product {product.id}: {name}"
                )
                print(
                    f"          OLD: {product.image}"
                )
                print(
                    "          No safe replacement exists."
                )

                product.image = None

                cleared += 1

            else:

                print(
                    f"[MISSING] Product {product.id}: {name}"
                )
                print(
                    "          No suitable image available."
                )

            missing += 1

            continue

        # ----------------------------------------------------
        # 4. Unknown product
        # ----------------------------------------------------

        print()
        print(
            f"[REVIEW]  Product {product.id}: {name}"
        )
        print(
            f"          Database: {product.image}"
        )
        print(
            "          No automatic image assignment made."
        )

        missing += 1

    return (
        repaired,
        valid,
        cleared,
        missing,
    )


# ============================================================
# CATEGORY IMAGE REPAIR
# ============================================================

def repair_categories():

    print()
    print("=" * 70)
    print("CATEGORY IMAGE CHECK")
    print("=" * 70)

    available_images = get_images(
        CATEGORIES_DIR
    )

    available_relative = {
        p.relative_to(STATIC_ROOT).as_posix()
        for p in available_images
    }

    repaired = 0
    valid = 0
    missing = 0

    categories = (
        Category.query
        .order_by(Category.display_order.asc())
        .all()
    )

    for category in categories:

        name = category.name.strip()

        # ----------------------------------------------------
        # Existing image
        # ----------------------------------------------------

        if database_path_exists(category.image):

            print(
                f"[OK]      Category {category.id}: "
                f"{name} -> {category.image}"
            )

            valid += 1

            continue

        # ----------------------------------------------------
        # Known safe mapping
        # ----------------------------------------------------

        mapped_image = SAFE_CATEGORY_IMAGES.get(
            name
        )

        if mapped_image:

            if mapped_image in available_relative:

                old_path = category.image

                category.image = mapped_image

                print()
                print(
                    f"[AUTO]    Category {category.id}: {name}"
                )
                print(
                    f"          OLD: {old_path}"
                )
                print(
                    f"          NEW: {mapped_image}"
                )

                repaired += 1

                continue

        # ----------------------------------------------------
        # Missing
        # ----------------------------------------------------

        print()

        if category.image:

            print(
                f"[MISSING] Category {category.id}: {name}"
            )
            print(
                f"          Database: {category.image}"
            )

        else:

            print(
                f"[NO IMAGE] Category {category.id}: {name}"
            )

        print(
            "          No safe automatic match found."
        )

        missing += 1

    return (
        repaired,
        valid,
        missing,
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("EAGLE FURNITURE NGARA")
    print("SAFE AUTOMATIC IMAGE PATH MANAGER")
    print("=" * 70)

    print(
        f"Static directory: {STATIC_ROOT}"
    )

    print(
        f"Product images:   {PRODUCTS_DIR}"
    )

    print(
        f"Category images:  {CATEGORIES_DIR}"
    )

    # --------------------------------------------------------
    # Backup
    # --------------------------------------------------------

    backup_database()

    # --------------------------------------------------------
    # Database operations
    # --------------------------------------------------------

    with app.app_context():

        (
            product_repaired,
            product_valid,
            product_cleared,
            product_missing,
        ) = repair_products()

        (
            category_repaired,
            category_valid,
            category_missing,
        ) = repair_categories()

        changes = (
            product_repaired
            + product_cleared
            + category_repaired
        )

        if changes:

            db.session.commit()

            print()
            print(
                "[DATABASE] Changes saved successfully."
            )

        else:

            print()
            print(
                "[DATABASE] No changes were required."
            )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("IMAGE MANAGEMENT COMPLETE")
    print("=" * 70)

    print(
        f"Products repaired:   {product_repaired}"
    )

    print(
        f"Products valid:      {product_valid}"
    )

    print(
        f"Products cleared:    {product_cleared}"
    )

    print(
        f"Products missing:    {product_missing}"
    )

    print(
        f"Categories repaired: {category_repaired}"
    )

    print(
        f"Categories valid:    {category_valid}"
    )

    print(
        f"Categories missing:  {category_missing}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()