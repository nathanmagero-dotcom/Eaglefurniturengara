# ==========================================================
# Eagle Furniture Ngara
# Master Product Catalogue
# ==========================================================
#
# IMPORTANT:
# This file is the source catalogue for the database importer.
#
# Website prices must NOT be hardcoded in templates.
# The database will become the single source of truth for:
#
# - Product name
# - SKU
# - Price
# - Sale price
# - Category
# - Subcategory
# - Description
# - Images / gallery
# - Specifications
# - Product flags
# - SEO information
#
# ==========================================================


products = [

    # ======================================================
    # SOFAS
    # ======================================================

    {
        "id": 1,
        "sku": "SOF001",
        "name": "6 Seater L-Shaped Sofa",
        "category": "Sofas",
        "subcategory": "L-Shaped",
        "price": 50000,
        "sale_price": 44499,
        "image": "images/products/lshape1.jpg",
        "gallery": [
            "images/products/lshape1.jpg",
            "images/products/lshape2.jpg",
            "images/products/lshape4.jpg",
            "images/products/lshape5.jpg",
            "images/products/lshape6.jpg",
        ],
        "description": (
            "Modern custom-made L-shaped sofa built with a "
            "hardwood frame and high-density cushions for "
            "exceptional comfort."
        ),
        "material": "Seasoned Hardwood",
        "fabric": "Premium Fabric",
        "colour": "Custom Colours",
        "size": "6 Seater",
        "stock": 8,
        "featured": True,
        "best_seller": True,
        "new_arrival": False,
        "delivery": "Nationwide",
    },

    {
        "id": 2,
        "sku": "SOF002",
        "name": "5 Seater Modern Sofa",
        "category": "Sofas",
        "subcategory": "Modern",
        "price": 59000,
        "sale_price": 54999,
        "image": "images/products/sofa2.jpg",
        "gallery": [
            "images/products/sofa2.jpg",
            "images/products/sofa3.jpg",
            "images/products/sofa4.jpg",
            "images/products/sofa5.jpg",
            "images/products/sofa6.jpg",
            "images/products/sofa7.jpg",
        ],
        "description": (
            "Elegant modern sofa suitable for apartments "
            "and family homes."
        ),
        "material": "Hardwood",
        "fabric": "Premium Fabric",
        "colour": "Custom Colours",
        "size": "5 Seater",
        "stock": 12,
        "featured": True,
        "best_seller": True,
        "new_arrival": True,
        "delivery": "Nationwide",
    },

    {
        "id": 3,
        "sku": "SOF003",
        "name": "7 Seater Luxury Sofa",
        "category": "Sofas",
        "subcategory": "Luxury",
        "price": 75000,
        "sale_price": 72000,
        "image": "images/products/luxury1.jpg",
        "gallery": [
            "images/products/luxury1.jpg",
            "images/products/luxury2.jpg",
            "images/products/luxury3.jpg",
            "images/products/luxury4.jpg",
            "images/products/luxury5.jpg",
            "images/products/luxury6.jpg",
            "images/products/luxury7.jpg",
        ],
        "description": (
            "Luxury sofa designed for spacious living rooms "
            "with premium comfort and a refined finish."
        ),
        "material": "Mahogany Hardwood",
        "fabric": "Premium Fabric",
        "colour": "Custom Colours",
        "size": "7 Seater",
        "stock": 5,
        "featured": True,
        "best_seller": False,
        "new_arrival": True,
        "delivery": "Nationwide",
    },

    {
        "id": 4,
        "sku": "SOF004",
        "name": "3 Seater Chesterfield Sofa",
        "category": "Sofas",
        "subcategory": "Chesterfield",
        "price": 30000,
        "sale_price": 26000,
        "image": "images/products/3-seater-chesterfield-sofa.jpg",
        "gallery": [
            "images/products/3-seater-chesterfield-sofa.jpg",
            "images/products/4-seater-chesterfield-sofa2.jpg",
            "images/products/5-seater-chesterfield-sofa3.jpg",
            "images/products/6-seater-chesterfield-sofa4.jpg",
            "images/products/7-seater-chesterfield-sofa5.jpg",
            "images/products/5-seater-chesterfield-sofa6.jpg",
            "images/products/6-seater-chesterfield-sofa7.jpg",
        ],
        "description": (
            "Classic Chesterfield sofa with timeless "
            "button-tufted design."
        ),
        "material": "Hardwood",
        "fabric": "Leather",
        "colour": "Brown",
        "size": "3 Seater",
        "stock": 6,
        "featured": True,
        "best_seller": False,
        "new_arrival": False,
        "delivery": "Nationwide",
    },

    {
        "id": 5,
        "sku": "SOF005",
        "name": "7 Seater Recliner Sofa Set",
        "category": "Sofas",
        "subcategory": "Recliner",
        "price": 180000,
        "sale_price": 165000,
        "image": "images/products/recliner.jpg",
        "gallery": [
            "images/products/recliner.jpg",
            "images/products/recliner3.jpg",
            "images/products/recliner4.jpg",
            "images/products/recliner5.jpg",
            "images/products/recliner6.jpg",
            "images/products/recliner7.jpg",
        ],
        "description": (
            "Premium reclining sofa designed for maximum "
            "relaxation and comfort."
        ),
        "material": "Hardwood",
        "fabric": "Leather",
        "colour": "Black",
        "size": "7 Seater",
        "stock": 4,
        "featured": True,
        "best_seller": True,
        "new_arrival": True,
        "delivery": "Nationwide",
    },

    {
        "id": 26,
        "sku": "SOF006",
        "name": "U-Shaped Family Sofa",
        "category": "Sofas",
        "subcategory": "Luxury",
        "price": 110000,
        "image": "images/products/u-shaped sofa.jpg",
        "gallery": [
            "images/products/u-shaped sofa.jpg",
            "images/products/u-shaped sofa2.jpg",
            "images/products/u-shaped sofa3.jpg",
            "images/products/u-shaped sofa4.jpg",
            "images/products/u-shaped sofa5.jpg",
            "images/products/u-shaped sofa6.jpg",
            "images/products/u-shaped sofa7.jpg",
        ],
        "description": (
            "Luxury U-shaped sofa suitable for large family "
            "living rooms."
        ),
        "material": "Seasoned Hardwood",
        "colour": "Grey",
        "size": "8 Seater",
        "rating": 5.0,
        "reviews": 42,
        "stock": 5,
        "featured": True,
        "best_seller": True,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },


    # ======================================================
    # BEDS
    # ======================================================

    {
        "id": 6,
        "sku": "BED001",
        "name": "Queen Size Bed",
        "category": "Beds",
        "subcategory": "Queen",
        "price": 32000,
        "sale_price": 28000,
        "image": "images/products/bed1.jpg",
        "gallery": [
            "images/products/bed1.jpg",
            "images/products/bed2.jpg",
            "images/products/bed3.jpg",
            "images/products/bed4.jpg",
            "images/products/bed5.jpg",
            "images/products/bed6.jpg",
            "images/products/bed7.jpg",

        ],
        "description": (
            "Modern queen-size bed crafted from seasoned "
            "hardwood with an elegant headboard."
        ),
        "material": "Mahogany Hardwood",
        "fabric": "Wood Finish",
        "colour": "Walnut",
        "size": "Queen",
        "stock": 8,
        "featured": True,
        "best_seller": True,
        "new_arrival": False,
        "delivery": "Nationwide",
    },

    {
        "id": 7,
        "sku": "BED002",
        "name": "King Size Bed",
        "category": "Beds",
        "subcategory": "King",
        "price": 45000,
        "sale_price": 38000,
        "image": "images/products/king-size-bed.jpg",
        "gallery": [
            "images/products/king-size-bed.jpg",
            "images/products/king-size-bed2.jpg",
            "images/products/king-size-bed3.jpg",
            "images/products/king-size-bed4.jpg",
            "images/products/king-size-bed5.jpg",
            "images/products/king-size-bed6.jpg",
            "images/products/king-size-bed7.jpg",
        ],
        "description": (
            "Luxury king-size bed designed for spacious "
            "bedrooms."
        ),
        "material": "Hardwood",
        "fabric": "Wood Finish",
        "colour": "Custom Finish",
        "size": "King",
        "stock": 6,
        "featured": True,
        "best_seller": False,
        "new_arrival": True,
        "delivery": "Nationwide",
    },

    {
        "id": 8,
        "sku": "BED003",
        "name": "4x6 Storage Bed",
        "category": "Beds",
        "subcategory": "Standard",
        "price": 30000,
        "sale_price": 28000,
        "image": "images/products/bed.jpg",
        "gallery": [
            "images/products/bed.jpg",
            "images/products/bed1.jpg",
            "images/products/bed2.jpg",
            "images/products/bed3.jpg",
            "images/products/bed4.jpg",
            "images/products/bed5.jpg",
            "images/products/bed6.jpg",
            "images/products/bed7.jpg",
        ],
        "description": (
            "Affordable and durable 4x6 storage bed suitable "
            "for apartments and guest rooms."
        ),
        "material": "Hardwood",
        "fabric": "Wood Finish",
        "colour": "Mahogany",
        "size": "4x6",
        "stock": 12,
        "featured": False,
        "best_seller": True,
        "new_arrival": False,
        "delivery": "Nationwide",
    },

    {
        "id": 27,
        "sku": "BED004",
        "name": "Double Decker Bed",
        "category": "Beds",
        "subcategory": "Kids",
        "price": 55000,
        "sale_price": 52000,
        "image": "images/products/bunk-bed.jpg",
        "gallery": [
            "images/products/bunk-bed.jpg",
            "images/products/bunk-bed2.jpg",
            "images/products/bunk-bed3.jpg",
            "images/products/bunk-bed4.jpg",
            "images/products/bunk-bed5.jpg",
            "images/products/bunk-bed6.jpg",
            "images/products/bunk-bed7.jpg",
        ],
        "description": (
            "Strong hardwood bunk bed suitable for children."
        ),
        "material": "Mahogany Hardwood",
        "colour": "White",
        "size": "Double Decker",
        "stock": 8,
        "featured": True,
        "best_seller": False,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },


    # ======================================================
    # DINING SETS
    # ======================================================

    {
        "id": 9,
        "sku": "DIN001",
        "name": "4 Seater Dining Set",
        "category": "Dining Sets",
        "subcategory": "Dining",
        "price": 40000,
        "image": "images/products/dining.jpg",
        "gallery": [
            "images/products/dining.jpg",
            "images/products/dining2.jpg",
            "images/products/dining3.jpg",
            "images/products/dining4.jpg",
            "images/products/dining5.jpg",
            "images/products/dining6.jpg",
            "images/products/dining7.jpg",
        ],
        "description": (
            "Elegant four-seater dining set perfect for "
            "compact homes."
        ),
        "material": "Hardwood",
        "fabric": "Wood Finish",
        "colour": "Walnut",
        "size": "4 Seater",
        "stock": 7,
        "featured": True,
        "best_seller": False,
        "new_arrival": True,
        "delivery": "Nationwide",
    },

    {
        "id": 10,
        "sku": "DIN002",
        "name": "8 Seater Dining Set",
        "category": "Dining Sets",
        "subcategory": "Dining",
        "price": 75000,
        "image": "images/products/dining.jpg",
        "gallery": [
            "images/products/dining.jpg",
            "images/products/dining2.jpg",
            "images/products/dining3.jpg",
            "images/products/dining4.jpg",
            "images/products/dining5.jpg",
            "images/products/dining6.jpg",
            "images/products/dining7.jpg",
        ],
        "description": (
            "Beautiful 8-seater dining table built for "
            "everyday family dining."
        ),
        "material": "Hardwood",
        "fabric": "Wood Finish",
        "colour": "Oak",
        "size": "8 Seater",
        "stock": 9,
        "featured": True,
        "best_seller": True,
        "new_arrival": False,
        "delivery": "Nationwide",
    },

    {
        "id": 11,
        "sku": "DIN003",
        "name": "10 Seater Dining Set",
        "category": "Dining Sets",
        "subcategory": "Luxury",
        "price": 95000,
        "sale_price": 72000,
        "image": "images/products/dining.jpg",
        "gallery": [
            "images/products/dining.jpg",
            "images/products/dining2.jpg",
            "images/products/dining3.jpg",
            "images/products/dining4.jpg",
            "images/products/dining5.jpg",
            "images/products/dining6.jpg",
            "images/products/dining7.jpg",
        ],
        "description": (
            "Luxury 10-seater dining set for larger "
            "families and entertaining."
        ),
        "material": "Mahogany Hardwood",
        "fabric": "Wood Finish",
        "colour": "Dark Walnut",
        "size": "10 Seater",
        "stock": 4,
        "featured": True,
        "best_seller": False,
        "new_arrival": True,
        "delivery": "Nationwide",
    },

    {
        "id": 28,
        "sku": "DIN004",
        "name": "3 Seater Dining Set",
        "category": "Dining Sets",
        "subcategory": "Luxury",
        "price": 28000,
        "sale_price": 24000,
        "image": "images/products/dining.jpg",
        "gallery": [
            "images/products/dining1.jpg",
            "images/products/dining2.jpg",
            "images/products/dining3.jpg",
            "images/products/dining4.jpg",
            "images/products/dining5.jpg",
            "images/products/dining6.jpg",
            "images/products/dining7.jpg",
        ],
        "description": (
            "Premium 3-seater dining set ideal for small "
            "homes."
        ),
        "material": "Mahogany Hardwood",
        "colour": "Walnut",
        "size": "3 Seater",
        "stock": 3,
        "featured": True,
        "best_seller": False,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },


    # ======================================================
    # TV UNITS
    # ======================================================

    {
        "id": 12,
        "sku": "TV001",
        "name": "Modern TV Unit",
        "category": "TV Units",
        "subcategory": "Modern",
        "price": 28000,
        "sale_price": 26000,
        "image": "images/products/tv1.jpg",
        "gallery": [
            "images/products/tv1.jpg",
            "images/products/tv2.jpg",
            "images/products/tv3.jpg",
            "images/products/tv4.jpg",
            "images/products/tv5.jpg",
            "images/products/tv6.jpg",
            "images/products/tv7.jpg",
        ],
        "description": (
            "Stylish TV unit with spacious storage for "
            "modern living rooms."
        ),
        "material": "MDF & Hardwood",
        "fabric": "Wood Finish",
        "colour": "White Walnut",
        "size": "180 cm",
        "stock": 10,
        "featured": True,
        "best_seller": True,
        "new_arrival": False,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },

    {
        "id": 13,
        "sku": "TV002",
        "name": "Floating TV Unit",
        "category": "TV Units",
        "subcategory": "Wall Mounted",
        "price": 28000,
        "sale_price": 25000,
        "image": "images/products/floating.jpg",
        "gallery": [
            "images/products/floating.jpg",
            "images/products/floating2.jpg",
            "images/products/floating3.jpg",
            "images/products/floating4.jpg",
            "images/products/floating5.jpg",
            "images/products/floating6.jpg",
            "images/products/floating7.jpg",
        ],
        "description": (
            "Wall-mounted floating TV unit with a sleek "
            "contemporary design."
        ),
        "material": "MDF",
        "fabric": "Wood Finish",
        "colour": "Gloss White",
        "size": "200 cm",
        "rating": 4.9,
        "reviews": 17,
        "stock": 5,
        "featured": False,
        "best_seller": False,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },

    {
        "id": 29,
        "sku": "TV003",
        "name": "Luxury Entertainment Unit",
        "category": "TV Units",
        "subcategory": "Luxury",
        "price": 32000,
        "sale_price": 28000,
        "image": "images/products/tv-luxury.jpg",
        "gallery": [
            "images/products/tv-luxury.jpg",
            "images/products/tv-luxury2.jpg",
            "images/products/tv-luxury3.jpg",
            "images/products/tv-luxury4.jpg",
            "images/products/tv-luxury5.jpg",
            "images/products/tv-luxury6.jpg",
            "images/products/tv-luxury7.jpg",
        ],
        "description": (
            "Large entertainment wall unit with shelves "
            "and storage."
        ),
        "material": "Hardwood",
        "colour": "Black Walnut",
        "size": "240 cm",
        "stock": 6,
        "featured": True,
        "best_seller": False,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },


    # ======================================================
    # COFFEE TABLES
    # ======================================================

    {
        "id": 14,
        "sku": "CT001",
        "name": "Modern Coffee Table",
        "category": "Coffee Tables",
        "subcategory": "Modern",
        "price": 18000,
        "sale_price": 16000,
        "image": "images/products/coffee1.jpg",
        "gallery": [
            "images/products/coffee1.jpg",
            "images/products/coffee2.jpg",
            "images/products/coffee3.jpg",
            "images/products/coffee4.jpg",
            "images/products/coffee5.jpg",
            "images/products/coffee6.jpg",
            "images/products/coffee7.jpg",
        ],
        "description": (
            "Minimalist coffee table with elegant wood finish."
        ),
        "material": "Hardwood",
        "fabric": "Wood Finish",
        "colour": "Walnut",
        "size": "Standard",
        "stock": 15,
        "featured": True,
        "best_seller": True,
        "new_arrival": False,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },

    {
        "id": 15,
        "sku": "CT002",
        "name": "Luxury Marble Coffee Table",
        "category": "Coffee Tables",
        "subcategory": "Luxury",
        "price": 24000,
        "sale_price": 22000,
        "image": "images/products/marble.jpg",
        "gallery": [
            "images/products/marble.jpg",
            "images/products/marble2.jpg",
            "images/products/marble3.jpg",
            "images/products/marble4.jpg",
            "images/products/marble5.jpg",
            "images/products/marble6.jpg",
            "images/products/marble7.jpg",
        ],
        "description": (
            "Premium marble-top coffee table that adds "
            "elegance to any living room."
        ),
        "material": "Marble & Metal",
        "fabric": "Marble Finish",
        "colour": "White",
        "size": "Large",
        "rating": 5.0,
        "reviews": 15,
        "stock": 6,
        "featured": True,
        "best_seller": False,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },


    # ======================================================
    # WARDROBES
    # ======================================================

    {
        "id": 16,
        "sku": "WRD001",
        "name": "2 Door Wardrobe",
        "category": "Wardrobes",
        "subcategory": "Bedroom",
        "price": 35000,
        "sale_price": 33000,
        "image": "images/products/wardrobe.jpg",
        "gallery": [
            "images/products/wardrobe.jpg",
            "images/products/wardrobe2.jpg",
            "images/products/wardrobe3.jpg",
            "images/products/wardrobe4.jpg",
            "images/products/wardrobe5.jpg",
            "images/products/wardrobe6.jpg",
            "images/products/wardrobe7.jpg",
        ],
        "description": (
            "Compact two-door wardrobe with hanging space "
            "and shelves."
        ),
        "material": "MDF & Hardwood",
        "colour": "Walnut",
        "size": "2 Door",
        "rating": 4.8,
        "reviews": 29,
        "stock": 10,
        "featured": True,
        "best_seller": True,
        "new_arrival": False,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },

    {
        "id": 17,
        "sku": "WRD002",
        "name": "luxury and modern Wardrobe",
        "category": "Wardrobes",
        "subcategory": "Bedroom",
        "price": 48000,
        "sale_price": 45000,
        "image": "images/products/modern wardrobe.jpg",
        "gallery": [
            "images/products/modern wardrobe.jpg",
            "images/products/modern wardrobe2.jpg",
            "images/products/modern wardrobe3.jpg",
            "images/products/modern wardrobe4.jpg",
            "images/products/modern wardrobe5.jpg",
            "images/products/modern wardrobe6.jpg",
            "images/products/modern wardrobe7.jpg",
        ],
        "description": (
            "Spacious wardrobe with shelves, drawers and "
            "hanging section."
        ),
        "material": "Hardwood",
        "colour": "Mahogany",
        "size": "3 Door",
        "rating": 4.9,
        "reviews": 34,
        "stock": 7,
        "featured": True,
        "best_seller": True,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },

    {
        "id": 18,
        "sku": "WRD003",
        "name": "Sliding Door Wardrobe",
        "category": "Wardrobes",
        "subcategory": "Luxury",
        "price": 68000,
        "sale_price": 65000,
        "image": "images/products/sliding.jpg",
        "gallery": [
            "images/products/sliding.jpg",
            "images/products/sliding2.jpg",
            "images/products/sliding3.jpg",
            "images/products/sliding4.jpg",
            "images/products/sliding5.jpg",
            "images/products/sliding6.jpg",
            "images/products/sliding7.jpg",
        ],
        "description": (
            "Modern sliding wardrobe ideal for contemporary "
            "bedrooms."
        ),
        "material": "MDF",
        "colour": "White",
        "size": "Large",
        "rating": 5.0,
        "reviews": 19,
        "stock": 5,
        "featured": True,
        "best_seller": False,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },

    {
        "id": 30,
        "sku": "WRD004",
        "name": "Walk-in Wardrobe System",
        "category": "Wardrobes",
        "subcategory": "Luxury",
        "price": 35000,
        "sale_price": 32000,
        "image": "images/products/walk-in.jpg",
        "gallery": [
            "images/products/walk-in.jpg",
            "images/products/walk-in2.jpg",
            "images/products/walk-in3.jpg",
            "images/products/walk-in4.jpg",
            "images/products/walk-in5.jpg",
            "images/products/walk-in6.jpg",
            "images/products/walk-in7.jpg"
        ],
        "description": (
            "Custom-made walk-in wardrobe system with drawers "
            "and shelves."
        ),
        "material": "Premium MDF",
        "colour": "Custom Finish",
        "size": "Custom",
        "rating": 5.0,
        "reviews": 8,
        "stock": 2,
        "featured": True,
        "best_seller": False,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "5 Years",
    },


    # ======================================================
    # OFFICE FURNITURE
    # ======================================================

    {
        "id": 19,
        "sku": "OFF001",
        "name": "Executive Office Desk",
        "category": "Office Furniture",
        "subcategory": "Office Desk",
        "price": 17000,
        "sale_price": 15000,
        "image": "images/products/office-desk.jpg",
        "gallery": [
            "images/products/office-desk.jpg",
            "images/products/office-desk2.jpg",
            "images/products/office-desk3.jpg",
            "images/products/office-desk4.jpg",
            "images/products/office-desk5.jpg",
            "images/products/office-desk6.jpg",
            "images/products/office-desk7.jpg",
        ],
        "description": (
            "Professional executive office desk with drawers "
            "and cable management."
        ),
        "material": "MDF & Metal",
        "colour": "Walnut",
        "size": "160 cm",
        "stock": 9,
        "featured": True,
        "best_seller": True,
        "new_arrival": False,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },

    {
        "id": 20,
        "sku": "OFF002",
        "name": "Ergonomic Office Chair",
        "category": "Office Furniture",
        "subcategory": "Office Chair",
        "price": 9000,
        "sale_price": 6500,
        "image": "images/products/office-chair.jpg",
        "gallery": [
            "images/products/office-chair.jpg",
            "images/products/office-chair2.jpg",
            "images/products/office-chair3.jpg",
            "images/products/office-chair4.jpg",
            "images/products/office-chair5.jpg",
            "images/products/office-chair6.jpg",
            "images/products/office-chair7.jpg",
        ],
        "description": (
            "Comfortable ergonomic chair with adjustable "
            "height and lumbar support."
        ),
        "material": "Mesh & Steel",
        "colour": "Black",
        "size": "Standard",
        "rating": 4.8,
        "reviews": 41,
        "stock": 15,
        "featured": True,
        "best_seller": True,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },


    # ======================================================
    # MATTRESSES
    # ======================================================

    {
        "id": 21,
        "sku": "MAT001",
        "name": "6x6 Orthopedic Mattress",
        "category": "Mattresses",
        "subcategory": "Orthopedic",
        "price": 16000,
        "image": "images/categories/mattressess.jpg",
        "gallery": [
            "images/categories/mattressess.jpg",
            "images/categories/mattressess2.jpg",
            "images/categories/mattressess3.jpg",
            "images/categories/mattressess4.jpg",
            "images/categories/mattressess5.jpg",
            "images/categories/mattressess6.jpg",
            "images/categories/mattressess7.jpg",
        ],
        "description": (
            "Premium orthopedic mattress offering excellent "
            "back support."
        ),
        "material": "High Density Foam",
        "colour": "White",
        "size": "6x6",
        "rating": 4.9,
        "reviews": 37,
        "stock": 12,
        "featured": True,
        "best_seller": True,
        "new_arrival": False,
        "delivery": "Nationwide",
        "warranty": "5 Years",
    },

    {
        "id": 22,
        "sku": "MAT002",
        "name": "5x6 Spring Mattress",
        "category": "Mattresses",
        "subcategory": "Spring",
        "price": 15000,
        "sale_price": 12000,
        "image": "images/categories/spring.jpg",
        "gallery": [
            "images/categories/spring.jpg",
            "images/categories/spring2.jpg",
            "images/categories/spring3.jpg",
            "images/categories/spring4.jpg",
            "images/categories/spring5.jpg",
            "images/categories/spring6.jpg",
            "images/categories/spring7.jpg",
        ],
        "description": (
            "Comfortable spring mattress designed for "
            "everyday use."
        ),
        "material": "Spring Foam",
        "colour": "White",
        "size": "5x6",
        "stock": 18,
        "featured": False,
        "best_seller": True,
        "new_arrival": False,
        "delivery": "Nationwide",
        "warranty": "5 Years",
    },


    # ======================================================
    # OUTDOOR FURNITURE
    # ======================================================

    {
        "id": 23,
        "sku": "OUT001",
        "name": "Outdoor Patio Set",
        "category": "Outdoor Furniture",
        "subcategory": "Patio",
        "price": 58000,
        "sale_price": 55000,
        "image": "images/categories/modern-outdoor1.jpg",
        "gallery": [
            "images/categories/modern-outdoor1.jpg",
            "images/categories/modern-outdoor2.jpg",
            "images/categories/modern-outdoor3.jpg",
            "images/categories/modern-outdoor4.jpg",
            "images/categories/modern-outdoor5.jpg",
            "images/categories/modern-outdoor6.jpg",
            "images/categories/modern_outdoor7.jpg",
        ],
        "description": (
            "Weather-resistant patio set perfect for gardens "
            "and balconies."
        ),
        "material": "Rattan",
        "colour": "Grey",
        "size": "4 Seater",
        "rating": 4.8,
        "reviews": 18,
        "stock": 6,
        "featured": True,
        "best_seller": False,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },

    {
        "id": 24,
        "sku": "OUT002",
        "name": "Outdoor, classic tables and Chair",
        "category": "Outdoor Furniture",
        "subcategory": "Patio",
        "price": 36000,
        "sale_price": 32000,
        "image": "images/categories/outdoor1.jpg",
        "gallery": [
            "images/categories/outdoor1.jpg",
            "images/categories/outdoor2.jpg",
            "images/categories/outdoor3.jpg",
            "images/categories/outdoor4.jpg",
            "images/categories/outdoor5.jpg",
            "images/categories/outdoor6.jpg",
            "images/categories/outdoor7.jpg",
        ],
        "description": (
            "Stylish outdoor tables and chairs for indoor and outdoor "
            "relaxation."
        ),
        "material": "Rattan & Steel",
        "colour": "Brown",
        "size": "Single",
        "rating": 4.9,
        "reviews": 16,
        "stock": 7,
        "featured": True,
        "best_seller": True,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "2 Years",
    },


    # ======================================================
    # HOME ACCESSORIES
    # ======================================================

    {
        "id": 25,
        "sku": "ACC001",
        "name": "Decorative Wall Mirror",
        "category": "Home Accessories",
        "subcategory": "Mirror",
        "price": 9500,
        "sale_price": 8500,
        "image": "images/products/mirror.jpg",
        "gallery": [
            "images/products/mirror.jpg",
            "images/products/mirror2.jpg",
            "images/products/mirror3.jpg",
            "images/products/mirror4.jpg",
            "images/products/mirror5.jpg",
            "images/products/mirror6.jpg",
            "images/products/mirror7.jpg",
        ],
        "description": (
            "Elegant decorative mirror that complements "
            "any room."
        ),
        "material": "Glass & Wood",
        "colour": "Gold",
        "size": "80 cm",
        "stock": 20,
        "featured": False,
        "best_seller": True,
        "new_arrival": True,
        "delivery": "Nationwide",
        "warranty": "1 Year",
    },

]


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def get_all_products():
    """Return all products in the master catalogue."""
    return products


def get_product_by_id(product_id):
    """Return a product by its catalogue ID."""

    return next(
        (
            product
            for product in products
            if product["id"] == product_id
        ),
        None,
    )


def get_product_by_sku(sku):
    """Return a product by SKU."""

    if not sku:
        return None

    sku = str(sku).strip().upper()

    return next(
        (
            product
            for product in products
            if str(product.get("sku", "")).strip().upper() == sku
        ),
        None,
    )


def get_featured_products():
    """Return featured products."""

    return [
        product
        for product in products
        if product.get("featured") is True
    ]


def get_best_sellers():
    """Return best-selling products."""

    return [
        product
        for product in products
        if product.get("best_seller") is True
    ]


def get_new_arrivals():
    """Return new arrival products."""

    return [
        product
        for product in products
        if product.get("new_arrival") is True
    ]


def get_products_by_category(category):
    """Return products belonging to a category."""

    if not category:
        return []

    category = str(category).strip().lower()

    return [
        product
        for product in products
        if str(product.get("category", "")).strip().lower()
        == category
    ]


def get_products_by_subcategory(subcategory):
    """Return products belonging to a subcategory."""

    if not subcategory:
        return []

    subcategory = str(subcategory).strip().lower()

    return [
        product
        for product in products
        if str(product.get("subcategory", "")).strip().lower()
        == subcategory
    ]


def search_products(query):
    """
    Search products by name, SKU, category,
    subcategory or description.
    """

    if not query:
        return products

    query = str(query).strip().lower()

    return [
        product
        for product in products
        if (
            query in str(product.get("name", "")).lower()
            or query in str(product.get("sku", "")).lower()
            or query in str(product.get("category", "")).lower()
            or query in str(product.get("subcategory", "")).lower()
            or query in str(product.get("description", "")).lower()
        )
    ]

# ==========================================================
# CATALOGUE VALIDATION
# ==========================================================

def validate_catalogue():
    """
    Validate the master catalogue for common importer problems.

    Returns:
        list[str]: Empty list means the catalogue is valid.
    """

    errors = []

    ids = set()
    skus = set()
    slugs = set()

    required_fields = (
        "id",
        "sku",
        "name",
        "category",
        "subcategory",
        "price",
        "image",
        "gallery",
        "description",
    )

    for index, product in enumerate(products, start=1):

        prefix = f"Product #{index}"

        # Required fields
        for field in required_fields:
            if not product.get(field):
                errors.append(
                    f"{prefix}: missing '{field}'"
                )

        # Duplicate ID
        product_id = product.get("id")

        if product_id in ids:
            errors.append(
                f"{prefix}: duplicate id '{product_id}'"
            )

        ids.add(product_id)

        # Duplicate SKU
        sku = str(
            product.get("sku", "")
        ).strip().upper()

        if sku in skus:
            errors.append(
                f"{prefix}: duplicate SKU '{sku}'"
            )

        skus.add(sku)

        # Slug
        slug = product.get("slug")

        if not slug:
            slug = slugify(
                product.get("name", "")
            )

        if slug in slugs:
            errors.append(
                f"{prefix}: duplicate slug '{slug}'"
            )

        slugs.add(slug)

        # Price validation
        price = product.get("price")
        sale_price = product.get("sale_price")

        if price is not None and price < 0:
            errors.append(
                f"{prefix}: negative price"
            )

        if sale_price is not None and sale_price < 0:
            errors.append(
                f"{prefix}: negative sale price"
            )

        if (
            price is not None
            and sale_price is not None
            and sale_price >= price
        ):
            errors.append(
                f"{prefix}: sale_price must be lower than price"
            )

        # Gallery validation
        gallery = product.get("gallery") or []

        if not gallery:
            errors.append(
                f"{prefix}: gallery is empty"
            )

        if (
            product.get("image")
            and product["image"] not in gallery
        ):
            errors.append(
                f"{prefix}: main image is missing from gallery"
            )

    return errors
