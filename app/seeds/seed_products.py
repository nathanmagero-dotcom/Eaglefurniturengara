from app.extensions import db
from app.models.category import Category
from app.models.product import Product


def seed_products():

    sofas = Category.query.filter_by(name="Sofas").first()

    beds = Category.query.filter_by(name="Beds").first()

    dining = Category.query.filter_by(name="Dining Sets").first()

    products = [

        Product(

            category=sofas,

            name="6 Seater L-Shaped Sofa",

            slug="6-seater-l-shaped-sofa",

            sku="SOF001",

            description="Premium custom-made L-shaped sofa.",

            price=65000,

            sale_price=62000,

            stock=8,

            material="Hardwood",

            colour="Grey",

            size="6 Seater",

            image="images/products/lshape1.jpg",

            featured=True,

            best_seller=True,

            new_arrival=True,

            rating=5,

            reviews=26,

            warranty="2 Years",

            delivery="Nationwide"

        ),

        Product(

            category=beds,

            name="Queen Size Bed",

            slug="queen-size-bed",

            sku="BED001",

            description="Premium hardwood queen bed.",

            price=42000,

            sale_price=39000,

            stock=12,

            material="Mahogany",

            colour="Walnut",

            size="5x6",

            image="images/products/bed1.jpg",

            featured=True,

            best_seller=True,

            rating=4.9,

            reviews=18,

            warranty="2 Years",

            delivery="Nationwide"

        ),

        Product(

            category=dining,

            name="6 Seater Dining Set",

            slug="6-seater-dining-set",

            sku="DIN001",

            description="Elegant dining set.",

            price=60000,

            sale_price=56000,

            stock=6,

            material="Mahogany",

            colour="Brown",

            size="6 Seater",

            image="images/products/dining1.jpg",

            featured=True,

            best_seller=True,

            rating=5,

            reviews=15,

            warranty="2 Years",

            delivery="Nationwide"

        )

    ]

    for product in products:

        exists = Product.query.filter_by(
            sku=product.sku
        ).first()

        if not exists:

            db.session.add(product)

    db.session.commit()

    print("Products seeded successfully.")