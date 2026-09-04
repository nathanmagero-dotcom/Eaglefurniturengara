import json
import sqlite3
import sys


DB_PATH = "/app/instance/app.db"
EXPORT_PATH = "catalogue_export.json"


def main():
    print("Loading catalogue export...")

    with open(EXPORT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = data["categories"]
    subcategories = data["subcategories"]
    products = data["products"]

    print(f"Categories to import: {len(categories)}")
    print(f"Subcategories to import: {len(subcategories)}")
    print(f"Products to import: {len(products)}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        # Safety check
        existing_products = conn.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        if existing_products > 0:
            print(
                f"STOP: Railway already contains {existing_products} products."
            )
            print("Nothing was changed.")
            sys.exit(1)

        # --------------------------------------------------
        # CATEGORIES
        # --------------------------------------------------

        for c in categories:
            conn.execute(
                """
                INSERT INTO categories
                (id, name, slug, description, image, active, display_order)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    c["id"],
                    c["name"],
                    c["slug"],
                    c["description"],
                    c["image"],
                    c["active"],
                    c["display_order"],
                ),
            )

        # --------------------------------------------------
        # SUBCATEGORIES
        # --------------------------------------------------

        for s in subcategories:
            conn.execute(
                """
                INSERT INTO subcategories
                (id, category_id, name, slug, description,
                 icon, image, active, display_order)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    s["id"],
                    s["category_id"],
                    s["name"],
                    s["slug"],
                    s["description"],
                    s["icon"],
                    s["image"],
                    s["active"],
                    s["display_order"],
                ),
            )

        # --------------------------------------------------
        # PRODUCTS
        # --------------------------------------------------

        for p in products:
            conn.execute(
                """
                INSERT INTO products
                (
                    id,
                    category_id,
                    name,
                    slug,
                    description,
                    price,
                    sale_price,
                    image,
                    featured,
                    best_seller,
                    new_arrival,
                    active,
                    subcategory_id,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    p["id"],
                    p["category_id"],
                    p["name"],
                    p["slug"],
                    p["description"],
                    p["price"],
                    p["sale_price"],
                    p["image"],
                    p["featured"],
                    p["best_seller"],
                    p["new_arrival"],
                    1,
                    p["subcategory_id"],
                    p["created_at"],
                    p["updated_at"],
                ),
            )

        conn.commit()

        print("")
        print("CATALOGUE IMPORT SUCCESSFUL")
        print(f"Categories: {len(categories)}")
        print(f"Subcategories: {len(subcategories)}")
        print(f"Products: {len(products)}")

    except Exception:
        conn.rollback()
        print("")
        print("IMPORT FAILED — all changes rolled back.")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()