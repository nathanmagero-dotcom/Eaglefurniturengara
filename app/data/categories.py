# ==========================================================
# Eagle Furniture Ngara
# Product Categories
# ==========================================================

categories = [

    {
        "id": 1,
        "name": "Sofas",
        "slug": "sofas",
        "image": "images/categories/sofas.jpg",
        "description": "Modern, classic and custom-made sofas for every home.",
        "featured": True
    },

    {
        "id": 2,
        "name": "Beds",
        "slug": "beds",
        "image": "images/categories/beds.jpg",
        "description": "Premium wooden beds crafted for comfort and durability.",
        "featured": True
    },

    {
        "id": 3,
        "name": "Mattresses",
        "slug": "mattresses",
        "image": "images/categories/mattresses.jpg",
        "description": "Orthopedic, spring and premium mattresses for restful sleep.",
        "featured": True
    },

    {
        "id": 4,
        "name": "Dining Sets",
        "slug": "dining-sets",
        "image": "images/categories/dining.jpg",
        "description": "Stylish dining sets for every family size.",
        "featured": True
    },

    {
        "id": 5,
        "name": "TV Units",
        "slug": "tv-units",
        "image": "images/categories/tv-units.jpg",
        "description": "Modern TV stands and wall units with smart storage.",
        "featured": True
    },

    {
        "id": 6,
        "name": "Coffee Tables",
        "slug": "coffee-tables",
        "image": "images/categories/coffee-tables.jpg",
        "description": "Elegant coffee tables that complete your living room.",
        "featured": True
    },

    {
        "id": 7,
        "name": "Wardrobes",
        "slug": "wardrobes",
        "image": "images/categories/wardrobes.jpg",
        "description": "Sliding, hinged and custom wardrobes for every bedroom.",
        "featured": True
    },

    {
        "id": 8,
        "name": "Office Furniture",
        "slug": "office-furniture",
        "image": "images/categories/office.jpg",
        "description": "Executive desks, ergonomic chairs and office storage.",
        "featured": True
    },

    {
        "id": 9,
        "name": "Outdoor Furniture",
        "slug": "outdoor-furniture",
        "image": "images/categories/outdoor.jpg",
        "description": "Weather-resistant patio and garden furniture.",
        "featured": False
    },

    {
        "id": 10,
        "name": "Home Accessories",
        "slug": "home-accessories",
        "image": "images/categories/accessories.jpg",
        "description": "Mirrors, décor pieces and home accessories.",
        "featured": False
    },

    {
        "id": 11,
        "name": "Complete Furniture Packages",
        "slug": "complete-packages",
        "image": "images/categories/packages.jpg",
        "description": "Complete furniture solutions for bedsitters, apartments, homes, Airbnb and offices.",
        "featured": True
    }

]

# ==========================================================
# Featured Categories
# ==========================================================

featured_categories = [

    category

    for category in categories

    if category["featured"]

]

# ==========================================================
# Category Lookup
# ==========================================================

category_lookup = {

    category["slug"]: category

    for category in categories

}

# ==========================================================
# Category Names
# ==========================================================

category_names = [

    category["name"]

    for category in categories

]

# ==========================================================
# Total Categories
# ==========================================================

TOTAL_CATEGORIES = len(categories)