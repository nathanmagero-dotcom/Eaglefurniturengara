import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.extensions import db
from app.models.product import Product

app = create_app()

PRODUCTS = [
    {
        "sku": "SOF007",
        "name": "Modern 3-Seater Sofa",
        "slug": "modern-3-seater-sofa",
        "price": 64999,
        "sale_price": 54999,
        "category": "Sofas",
        "subcategory": "Modern Sofas",
        "image": None,
    },
    {
        "sku": "DIN005",
        "name": "Solid Wood Dining Table",
        "slug": "solid-wood-dining-table",
        "price": 34999,
        "sale_price": None,
        "category": "Dining Sets",
        "subcategory": "Dining",
        "image": None,
    },
    {
        "sku": "BED005",
        "name": "Queen Bed Frame",
        "slug": "queen-bed-frame",
        "price": 36999,
        "sale_price": 29999,
        "category": "Beds",
        "subcategory": "Queen",
        "image": None,
    },
]

with app.app_context():

    print("CATALOGUE EXPANSION CHECK")
    print("=" * 60)

    for item in PRODUCTS:

        existing = Product.query.filter_by(sku=item["sku"]).first()

        if existing:
            print(f"SKIP: {item['sku']} already exists")
            continue

        print(
            f"READY: {item['sku']} | "
            f"{item['name']} | "
            f"KSh {item['price']:,.0f}"
            + (
                f" -> KSh {item['sale_price']:,.0f}"
                if item["sale_price"] is not None
                else ""
            )
        )

    print()
    print("NO DATABASE CHANGES WERE MADE.")
    print("Images must be supplied before these products are imported.")
