from __future__ import annotations
import os, shutil
from datetime import datetime
from app import create_app
from app.extensions import db
from app.models.product import Product
from app.data.products import products as catalogue_products

app = create_app()

with app.app_context():
    static_root = app.static_folder
    backup_dir = os.path.join(app.instance_path, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    db_path = os.path.join(app.instance_path, "app.db")
    backup_path = os.path.join(backup_dir, f"app_before_image_sync_{stamp}.db")
    if os.path.exists(db_path):
        shutil.copy2(db_path, backup_path)
        print(f"Database backup: {backup_path}")

    by_name = {str(p.get("name", "")).strip().lower(): p for p in catalogue_products}
    changed, unresolved = [], []

    for product in Product.query.all():
        source = by_name.get((product.name or "").strip().lower())
        if not source:
            continue
        candidates = []
        if source.get("image"):
            candidates.append(source["image"])
        candidates.extend(source.get("gallery") or [])
        usable = next(
            (path for path in candidates
             if path and os.path.isfile(os.path.join(static_root, path))),
            None
        )
        if usable and product.image != usable:
            changed.append((product.id, product.name, product.image, usable))
            product.image = usable
        if product.active and (
            not product.image
            or not os.path.isfile(os.path.join(static_root, product.image))
        ):
            unresolved.append((product.id, product.name, product.image))

    db.session.commit()
    print(f"Updated image paths: {len(changed)}")
    for row in changed:
        print(row)
    print(f"Active products still without valid image: {len(unresolved)}")
    for row in unresolved:
        print(row)
    print("No products were deleted.")
