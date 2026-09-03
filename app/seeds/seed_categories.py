from app.extensions import db
from app.models.category import Category


def seed_categories():

    categories = [

        {
            "name": "Sofas",
            "slug": "sofas",
            "description": "Modern and custom-made sofas.",
            "image": "images/categories/sofas.jpg"
        },

        {
            "name": "Beds",
            "slug": "beds",
            "description": "Quality beds for every bedroom.",
            "image": "images/categories/beds.jpg"
        },

        {
            "name": "Dining Sets",
            "slug": "dining-sets",
            "description": "Elegant dining furniture.",
            "image": "images/categories/dining.jpg"
        },

        {
            "name": "TV Units",
            "slug": "tv-units",
            "description": "Modern entertainment units.",
            "image": "images/categories/tv.jpg"
        },

        {
            "name": "Coffee Tables",
            "slug": "coffee-tables",
            "description": "Stylish coffee tables.",
            "image": "images/categories/coffee.jpg"
        },

        {
            "name": "Wardrobes",
            "slug": "wardrobes",
            "description": "Modern wardrobes.",
            "image": "images/categories/wardrobe.jpg"
        },

        {
            "name": "Office Furniture",
            "slug": "office-furniture",
            "description": "Office desks and chairs.",
            "image": "images/categories/office.jpg"
        },

        {
            "name": "Mattresses",
            "slug": "mattresses",
            "description": "Premium mattresses.",
            "image": "images/categories/mattress.jpg"
        }

    ]

    for item in categories:

        exists = Category.query.filter_by(
            slug=item["slug"]
        ).first()

        if not exists:

            db.session.add(
                Category(**item)
            )

    db.session.commit()

    print("Categories seeded successfully.")