# ==========================================================
# Eagle Furniture Ngara
# Furniture Bundles
# ==========================================================

bundles = [

    {
        "id": 1,
        "name": "Bedsitter Package",
        "slug": "bedsitter-package",

        "price": 145000,
        "sale_price": 135000,
        "save": 10000,

        "image": "images/bundles/bedsitter.jpg",

        "featured": True,
        "popular": True,

        "description":
            "A complete furniture package designed for bedsitters and studio apartments.",

        "items": [

            "4x6 Bed",
            "Orthopedic Mattress",
            "2 Seater Sofa",
            "Coffee Table",
            "TV Stand",
            "2 Door Wardrobe"

        ],

        "rooms": 1,

        "pieces": 6,

        "delivery": "Nationwide",

        "warranty": "2 Years",

        "customizable": True
    },

    {
        "id": 2,
        "name": "One Bedroom Package",
        "slug": "one-bedroom-package",

        "price": 265000,
        "sale_price": 249000,
        "save": 16000,

        "image": "images/bundles/one-bedroom.jpg",

        "featured": True,
        "popular": True,

        "description":
            "Everything required to furnish a one-bedroom apartment.",

        "items": [

            "Queen Bed",
            "Orthopedic Mattress",
            "Bedside Tables",
            "3 Door Wardrobe",
            "5 Seater Sofa",
            "Coffee Table",
            "TV Unit",
            "4 Seater Dining Set"

        ],

        "rooms": 2,

        "pieces": 8,

        "delivery": "Nationwide",

        "warranty": "2 Years",

        "customizable": True
    },

    {
        "id": 3,
        "name": "Two Bedroom Package",
        "slug": "two-bedroom-package",

        "price": 420000,
        "sale_price": 395000,
        "save": 25000,

        "image": "images/bundles/two-bedroom.jpg",

        "featured": True,
        "popular": True,

        "description":
            "Ideal package for modern two-bedroom homes.",

        "items": [

            "Queen Bed",
            "Double Bed",
            "2 Mattresses",
            "2 Wardrobes",
            "6 Seater Sofa",
            "Coffee Table",
            "TV Unit",
            "6 Seater Dining Set"

        ],

        "rooms": 3,

        "pieces": 10,

        "delivery": "Nationwide",

        "warranty": "2 Years",

        "customizable": True
    },

    {
        "id": 4,
        "name": "Three Bedroom Package",
        "slug": "three-bedroom-package",

        "price": 620000,
        "sale_price": 590000,
        "save": 30000,

        "image": "images/bundles/three-bedroom.jpg",

        "featured": True,
        "popular": False,

        "description":
            "Luxury package for fully furnishing a three-bedroom home.",

        "items": [

            "King Bed",
            "Queen Bed",
            "Double Bed",
            "3 Mattresses",
            "3 Wardrobes",
            "Luxury Sofa",
            "Coffee Table",
            "TV Unit",
            "8 Seater Dining Set"

        ],

        "rooms": 4,

        "pieces": 13,

        "delivery": "Nationwide",

        "warranty": "2 Years",

        "customizable": True
    },

    {
        "id": 5,
        "name": "Airbnb Package",
        "slug": "airbnb-package",

        "price": 350000,
        "sale_price": 329000,
        "save": 21000,

        "image": "images/bundles/airbnb.jpg",

        "featured": True,
        "popular": True,

        "description":
            "Furniture package designed specifically for Airbnb hosts.",

        "items": [

            "Queen Bed",
            "Mattress",
            "Wardrobe",
            "Modern Sofa",
            "Coffee Table",
            "TV Unit",
            "Dining Set"

        ],

        "rooms": 2,

        "pieces": 8,

        "delivery": "Nationwide",

        "warranty": "2 Years",

        "customizable": True
    },

    {
        "id": 6,
        "name": "Office Package",
        "slug": "office-package",

        "price": 195000,
        "sale_price": 180000,
        "save": 15000,

        "image": "images/bundles/office.jpg",

        "featured": False,
        "popular": True,

        "description":
            "Complete office furniture starter package.",

        "items": [

            "Executive Desk",
            "Office Chair",
            "Reception Desk",
            "Office Cabinet",
            "Bookshelf"

        ],

        "rooms": 1,

        "pieces": 5,

        "delivery": "Nationwide",

        "warranty": "2 Years",

        "customizable": True
    }

]


# ==========================================================
# FEATURED BUNDLES
# ==========================================================

featured_bundles = [

    bundle

    for bundle in bundles

    if bundle["featured"]

]


# ==========================================================
# POPULAR BUNDLES
# ==========================================================

popular_bundles = [

    bundle

    for bundle in bundles

    if bundle["popular"]

]


# ==========================================================
# FIND BUNDLE BY SLUG
# ==========================================================

bundle_lookup = {

    bundle["slug"]: bundle

    for bundle in bundles

}


# ==========================================================
# FIND BUNDLE BY ID
# ==========================================================

bundle_by_id = {

    bundle["id"]: bundle

    for bundle in bundles

}


# ==========================================================
# TOTAL BUNDLES
# ==========================================================

TOTAL_BUNDLES = len(bundles)