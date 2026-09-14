"""
Eagle Furniture Ngara
Master Product Catalogue

This file is the catalogue source used by the product/database importer.
The homepage, collection pages and product pages should read product data
from the database after seeding/updating from this catalogue.

Do not hard-code individual products into templates.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Iterable, Optional


def slugify(value: str) -> str:
    """Create a stable URL-safe slug."""
    value = str(value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


products = [
    {'id': 1, 'sku': 'SOF001', 'name': '6 Seater L-Shaped Sofa', 'category': 'Sofas', 'subcategory': 'L-Shaped', 'price': 50000, 'sale_price': 44499, 'image': 'images/products/lshape1.jpg', 'gallery': ['images/products/lshape1.jpg', 'images/products/lshape2.jpg', 'images/products/lshape4.jpg', 'images/products/lshape5.jpg'], 'description': 'Modern custom-made L-shaped sofa built with a hardwood frame and high-density cushions for exceptional comfort.', 'material': 'Seasoned Hardwood', 'fabric': 'Premium Fabric', 'colour': 'Custom Colours', 'size': '6 Seater', 'stock': 8, 'featured': True, 'best_seller': True, 'new_arrival': False, 'delivery': 'Nationwide', 'slug': '6-seater-l-shaped-sofa', 'seo_title': '6 Seater L-Shaped Sofa | Eagle Furniture Ngara', 'seo_description': '6 Seater L-Shaped Sofa from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0, 'warranty': None},

    {'id': 2, 'sku': 'SOF002', 'name': '5 Seater Modern Sofa', 'category': 'Sofas', 'subcategory': 'Modern Sofas', 'price': 59000, 'sale_price': 54999, 'image': 'images/products/sofa2.jpg', 'gallery': ['images/products/sofa2.jpg', 'images/products/sofa3.jpg', 'images/products/sofa5.jpg'], 'description': 'Elegant modern sofa suitable for apartments and family homes.', 'material': 'Hardwood', 'fabric': 'Premium Fabric', 'colour': 'Custom Colours', 'size': '5 Seater', 'stock': 12, 'featured': True, 'best_seller': True, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': '5-seater-modern-sofa', 'seo_title': '5 Seater Modern Sofa | Eagle Furniture Ngara', 'seo_description': '5 Seater Modern Sofa from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0, 'warranty': None},

    {'id': 3, 'sku': 'SOF003', 'name': '7 Seater Luxury Sofa', 'category': 'Sofas', 'subcategory': 'Luxury Sofas', 'price': 75000, 'sale_price': 72000, 'image': 'images/products/luxury1.jpg', 'gallery': ['images/products/luxury1.jpg', 'images/products/luxury2.jpg', 'images/products/luxury3.jpg', 'images/products/luxury4.jpg', 'images/products/luxury5.jpg'], 'description': 'Luxury sofa designed for spacious living rooms with premium comfort and a refined finish.', 'material': 'Mahogany Hardwood', 'fabric': 'Premium Fabric', 'colour': 'Custom Colours', 'size': '7 Seater', 'stock': 5, 'featured': True, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': '7-seater-luxury-sofa', 'seo_title': '7 Seater Luxury Sofa | Eagle Furniture Ngara', 'seo_description': '7 Seater Luxury Sofa from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0, 'warranty': None},

    {'id': 4, 'sku': 'SOF004', 'name': '3 Seater Chesterfield Sofa', 'category': 'Sofas', 'subcategory': 'Chesterfield Sofas', 'price': 30000, 'sale_price': 26000, 'image': 'images/products/3-seater-chesterfield-sofa.jpg', 'gallery': ['images/products/3-seater-chesterfield-sofa.jpg'], 'description': 'Classic Chesterfield sofa with timeless button-tufted design.', 'material': 'Hardwood', 'fabric': 'Leather', 'colour': 'Brown', 'size': '3 Seater', 'stock': 6, 'featured': True, 'best_seller': False, 'new_arrival': False, 'delivery': 'Nationwide', 'slug': '3-seater-chesterfield-sofa', 'seo_title': '3 Seater Chesterfield Sofa | Eagle Furniture Ngara', 'seo_description': '3 Seater Chesterfield Sofa from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0, 'warranty': None},

    {'id': 5, 'sku': 'SOF005', 'name': '7 Seater Recliner Sofa Set', 'category': 'Sofas', 'subcategory': 'Recliner Sofas', 'price': 180000, 'sale_price': 165000, 'image': 'images/products/recliner.jpg', 'gallery': ['images/products/recliner.jpg', 'images/products/recliner3.jpg', 'images/products/recliner-sofa-set.jpg'], 'description': 'Premium reclining sofa designed for maximum relaxation and comfort.', 'material': 'Hardwood', 'fabric': 'Leather', 'colour': 'Black', 'size': '7 Seater', 'stock': 4, 'featured': True, 'best_seller': True, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': '7-seater-recliner-sofa-set', 'seo_title': '7 Seater Recliner Sofa Set | Eagle Furniture Ngara', 'seo_description': '7 Seater Recliner Sofa Set from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0, 'warranty': None},

    {'id': 26, 'sku': 'SOF006', 'name': 'U-Shaped Family Sofa', 'category': 'Sofas', 'subcategory': 'Luxury Sofas', 'price': 118000, 'sale_price': 110000, 'image': 'images/products/u-shaped sofa.jpg', 'gallery': ['images/products/u-shaped sofa.jpg'], 'description': 'Luxury U-shaped sofa suitable for large family living rooms.', 'material': 'Seasoned Hardwood', 'colour': 'Grey', 'size': '8 Seater', 'rating': 5.0, 'reviews': 42, 'stock': 5, 'featured': True, 'best_seller': True, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': 'u-shaped-family-sofa', 'seo_title': 'U-Shaped Family Sofa | Eagle Furniture Ngara', 'seo_description': 'U-Shaped Family Sofa from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.'},

    {'id': 6, 'sku': 'BED001', 'name': 'Queen Size Bed', 'category': 'Beds', 'subcategory': 'Queen Size Beds', 'price': 32000, 'sale_price': 28000, 'image': 'images/products/bed1.jpg', 'gallery': ['images/products/bed1.jpg', 'images/products/bed2.jpg', 'images/products/bed3.jpg', 'images/products/bed4.jpg'], 'description': 'Modern queen-size bed crafted from seasoned hardwood with an elegant headboard.', 'material': 'Mahogany Hardwood', 'fabric': 'Wood Finish', 'colour': 'Walnut', 'size': 'Queen', 'stock': 8, 'featured': True, 'best_seller': True, 'new_arrival': False, 'delivery': 'Nationwide', 'slug': 'queen-size-bed', 'seo_title': 'Queen Size Bed | Eagle Furniture Ngara', 'seo_description': 'Queen Size Bed from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0, 'warranty': None},

    {'id': 7, 'sku': 'BED002', 'name': 'King Size Bed', 'category': 'Beds', 'subcategory': 'King Size Beds', 'price': 45000, 'sale_price': 38000, 'image': 'images/products/king-size-bed.jpg', 'gallery': ['images/products/king-size-bed.jpg'], 'description': 'Luxury king-size bed designed for spacious bedrooms.', 'material': 'Hardwood', 'fabric': 'Wood Finish', 'colour': 'Custom Finish', 'size': 'King', 'stock': 6, 'featured': True, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'king-size-bed', 'seo_title': 'King Size Bed | Eagle Furniture Ngara', 'seo_description': 'King Size Bed from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0, 'warranty': None},

    {'id': 8, 'sku': 'BED003', 'name': '4x6 Storage Bed', 'category': 'Beds', 'subcategory': '4x6 Beds', 'price': 30000, 'sale_price': 28000, 'image': 'images/products/bed.jpg', 'gallery': ['images/products/bed.jpg', 'images/products/bed1.jpg', 'images/products/bed2.jpg', 'images/products/bed3.jpg', 'images/products/bed4.jpg'], 'description': 'Affordable and durable 4x6 storage bed suitable for apartments and guest rooms.', 'material': 'Hardwood', 'fabric': 'Wood Finish', 'colour': 'Mahogany', 'size': '4x6', 'stock': 12, 'featured': False, 'best_seller': True, 'new_arrival': False, 'delivery': 'Nationwide', 'slug': '4x6-storage-bed', 'seo_title': '4x6 Storage Bed | Eagle Furniture Ngara', 'seo_description': '4x6 Storage Bed from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0, 'warranty': None},

    {'id': 27, 'sku': 'BED004', 'name': 'Double Decker Bed', 'category': 'Beds', 'subcategory': 'Kids Beds', 'price': 55000, 'sale_price': 52000, 'image': 'images/products/bunk-bed.jpg', 'gallery': ['images/products/bunk-bed.jpg'], 'description': 'Strong hardwood bunk bed suitable for children.', 'material': 'Mahogany Hardwood', 'colour': 'White', 'size': 'Double Decker', 'stock': 8, 'featured': True, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': 'double-decker-bed', 'seo_title': 'Double Decker Bed | Eagle Furniture Ngara', 'seo_description': 'Double Decker Bed from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0},

    {'id': 9, 'sku': 'DIN001', 'name': '4 Seater Dining Set', 'category': 'Dining Sets', 'subcategory': '4-Seater Dining Sets', 'price': 40000, 'image': 'images/products/dining04.jpg', 'gallery': ['images/products/dining04.jpg', 'images/products/dining10.jpg'], 'description': 'Elegant four-seater dining set perfect for compact homes.', 'material': 'Hardwood', 'fabric': 'Wood Finish', 'colour': 'Walnut', 'size': '4 Seater', 'stock': 7, 'featured': True, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': '4-seater-dining-set', 'seo_title': '4 Seater Dining Set | Eagle Furniture Ngara', 'seo_description': '4 Seater Dining Set from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0, 'sale_price': None, 'warranty': None},

    {'id': 10, 'sku': 'DIN002', 'name': '6 Seater Dining Set', 'category': 'Dining Sets', 'subcategory': '6-Seater Dining Sets', 'price': 55000, 'image': 'images/products/dining-set.jpg', 'gallery': ['images/products/dining-set.jpg', 'images/products/dining04.jpg', 'images/products/dining10.jpg'], 'description': 'Beautiful six-seater dining table built for everyday family dining.', 'material': 'Hardwood', 'fabric': 'Wood Finish', 'colour': 'Oak', 'size': '6 Seater', 'stock': 9, 'featured': True, 'best_seller': True, 'new_arrival': False, 'delivery': 'Nationwide', 'slug': '6-seater-dining-set', 'seo_title': '6 Seater Dining Set | Eagle Furniture Ngara', 'seo_description': '6 Seater Dining Set from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0, 'sale_price': None, 'warranty': None},

    {'id': 11, 'sku': 'DIN003', 'name': '8 Seater Dining Set', 'category': 'Dining Sets', 'subcategory': '8-Seater Dining Sets', 'price': 75000, 'sale_price': 72000, 'image': 'images/products/dining-set.jpg', 'gallery': ['images/products/dining10.jpg', 'images/products/dining-set.jpg'], 'description': 'Luxury eight-seater dining set for larger families and entertaining.', 'material': 'Mahogany Hardwood', 'fabric': 'Wood Finish', 'colour': 'Dark Walnut', 'size': '8 Seater', 'stock': 4, 'featured': True, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': '8-seater-dining-set', 'seo_title': '8 Seater Dining Set | Eagle Furniture Ngara', 'seo_description': '8 Seater Dining Set from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0, 'warranty': None},

    {'id': 28, 'sku': 'DIN004', 'name': '10 Seater Dining Set', 'category': 'Dining Sets', 'subcategory': '10-Seater Dining Sets', 'price': 115000, 'sale_price': 109000, 'image': 'images/products/dining10.jpg', 'gallery': ['images/products/dining10.jpg'], 'description': 'Premium 10-seater dining set ideal for large homes.', 'material': 'Mahogany Hardwood', 'colour': 'Walnut', 'size': '10 Seater', 'stock': 3, 'featured': True, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': '10-seater-dining-set', 'seo_title': '10 Seater Dining Set | Eagle Furniture Ngara', 'seo_description': '10 Seater Dining Set from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0},

    {'id': 12, 'sku': 'TV001', 'name': 'Modern TV Unit', 'category': 'TV Units', 'subcategory': 'Modern TV Units', 'price': 28000, 'sale_price': 26000, 'image': 'images/products/tv1.jpg', 'gallery': ['images/products/tv1.jpg', 'images/products/tv-unit.jpg', 'images/products/tv-luxury.jpg', 'images/products/modern-tv-unit.jpg'], 'description': 'Stylish TV unit with spacious storage for modern living rooms.', 'material': 'MDF & Hardwood', 'fabric': 'Wood Finish', 'colour': 'White Walnut', 'size': '180 cm', 'stock': 10, 'featured': True, 'best_seller': True, 'new_arrival': False, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': 'modern-tv-unit', 'seo_title': 'Modern TV Unit | Eagle Furniture Ngara', 'seo_description': 'Modern TV Unit from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0},

    {'id': 13, 'sku': 'TV002', 'name': 'Floating TV Unit', 'category': 'TV Units', 'subcategory': 'Floating TV Units', 'price': 28000, 'sale_price': 25000, 'image': 'images/products/floating-tv-unit.jpg', 'gallery': ['images/products/floating-tv-unit.jpg'], 'description': 'Wall-mounted floating TV unit with a sleek contemporary design.', 'material': 'MDF', 'fabric': 'Wood Finish', 'colour': 'Gloss White', 'size': '200 cm', 'rating': 4.9, 'reviews': 17, 'stock': 5, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': 'floating-tv-unit', 'seo_title': 'Floating TV Unit | Eagle Furniture Ngara', 'seo_description': 'Floating TV Unit from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.'},

    {'id': 29, 'sku': 'TV003', 'name': 'Luxury Entertainment Unit', 'category': 'TV Units', 'subcategory': 'Luxury TV Units', 'price': 52000, 'sale_price': 49000, 'image': 'images/products/tv-luxury.jpg', 'gallery': ['images/products/tv-luxury.jpg'], 'description': 'Large entertainment wall unit with shelves and storage.', 'material': 'Hardwood', 'colour': 'Black Walnut', 'size': '240 cm', 'stock': 6, 'featured': True, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': 'luxury-entertainment-unit', 'seo_title': 'Luxury Entertainment Unit | Eagle Furniture Ngara', 'seo_description': 'Luxury Entertainment Unit from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0},

    {'id': 14, 'sku': 'CT001', 'name': 'Modern Coffee Table', 'category': 'Coffee Tables', 'subcategory': 'Modern Coffee Tables', 'price': 18000, 'sale_price': 16000, 'image': 'images/products/coffee1.jpg', 'gallery': ['images/products/coffee1.jpg'], 'description': 'Minimalist coffee table with elegant wood finish.', 'material': 'Hardwood', 'fabric': 'Wood Finish', 'colour': 'Walnut', 'size': 'Standard', 'stock': 15, 'featured': True, 'best_seller': True, 'new_arrival': False, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': 'modern-coffee-table', 'seo_title': 'Modern Coffee Table | Eagle Furniture Ngara', 'seo_description': 'Modern Coffee Table from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0},

    {'id': 15, 'sku': 'CT002', 'name': 'Luxury Marble Coffee Table', 'category': 'Coffee Tables', 'subcategory': 'Marble Coffee Tables', 'price': 24000, 'sale_price': 22000, 'image': 'images/products/luxury-marble-coffee-table.jpg', 'gallery': ['images/products/luxury-marble-coffee-table.jpg'], 'description': 'Premium marble-top coffee table that adds elegance to any living room.', 'material': 'Marble & Metal', 'fabric': 'Marble Finish', 'colour': 'White', 'size': 'Large', 'rating': 5.0, 'reviews': 15, 'stock': 6, 'featured': True, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': 'luxury-marble-coffee-table', 'seo_title': 'Luxury Marble Coffee Table | Eagle Furniture Ngara', 'seo_description': 'Luxury Marble Coffee Table from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.'},

    {'id': 16, 'sku': 'WRD001', 'name': '2 Door Wardrobe', 'category': 'Wardrobes', 'subcategory': '2-Door Wardrobes', 'price': 35000, 'sale_price': 33000, 'image': 'images/products/wardrobe2.jpg', 'gallery': ['images/products/wardrobe2.jpg'], 'description': 'Compact two-door wardrobe with hanging space and shelves.', 'material': 'MDF & Hardwood', 'colour': 'Walnut', 'size': '2 Door', 'rating': 4.8, 'reviews': 29, 'stock': 10, 'featured': True, 'best_seller': True, 'new_arrival': False, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': '2-door-wardrobe', 'seo_title': '2 Door Wardrobe | Eagle Furniture Ngara', 'seo_description': '2 Door Wardrobe from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.'},

    {'id': 17, 'sku': 'WRD002', 'name': '3 Door Wardrobe', 'category': 'Wardrobes', 'subcategory': '3-Door Wardrobes', 'price': 48000, 'sale_price': 45000, 'image': 'images/products/3-door-wardrobe.jpg', 'gallery': ['images/products/3-door-wardrobe.jpg'], 'description': 'Spacious wardrobe with shelves, drawers and hanging section.', 'material': 'Hardwood', 'colour': 'Mahogany', 'size': '3 Door', 'rating': 4.9, 'reviews': 34, 'stock': 7, 'featured': True, 'best_seller': True, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': '3-door-wardrobe', 'seo_title': '3 Door Wardrobe | Eagle Furniture Ngara', 'seo_description': '3 Door Wardrobe from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.'},

    {'id': 18, 'sku': 'WRD003', 'name': 'Sliding Door Wardrobe', 'category': 'Wardrobes', 'subcategory': 'Sliding Door Wardrobes', 'price': 68000, 'sale_price': 65000, 'image': 'images/products/sliding-door-wardrobe.jpg', 'gallery': ['images/products/sliding-door-wardrobe.jpg'], 'description': 'Modern sliding wardrobe ideal for contemporary bedrooms.', 'material': 'MDF', 'colour': 'White', 'size': 'Large', 'rating': 5.0, 'reviews': 19, 'stock': 5, 'featured': True, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': 'sliding-door-wardrobe', 'seo_title': 'Sliding Door Wardrobe | Eagle Furniture Ngara', 'seo_description': 'Sliding Door Wardrobe from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.'},

    {'id': 30, 'sku': 'WRD004', 'name': 'Walk-in Wardrobe System', 'category': 'Wardrobes', 'subcategory': 'Walk-In Wardrobes', 'price': 75000, 'sale_price': 68000, 'image': 'images/products/3-door-wardrobe.jpg', 'gallery': ['images/products/3-door-wardrobe.jpg'], 'description': 'Custom-made walk-in wardrobe system with drawers and shelves.', 'material': 'Premium MDF', 'colour': 'Custom Finish', 'size': 'Custom', 'rating': 5.0, 'reviews': 8, 'stock': 2, 'featured': True, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '5 Years', 'slug': 'walk-in-wardrobe-system', 'seo_title': 'Walk-in Wardrobe System | Eagle Furniture Ngara', 'seo_description': 'Walk-in Wardrobe System from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.'},

    {'id': 19, 'sku': 'OFF001', 'name': 'Executive Office Desk', 'category': 'Office Furniture', 'subcategory': 'Executive Desks', 'price': 17000, 'sale_price': 15000, 'image': 'images/products/office-desk.jpg', 'gallery': ['images/products/office-desk.jpg'], 'description': 'Professional executive office desk with drawers and cable management.', 'material': 'MDF & Metal', 'colour': 'Walnut', 'size': '160 cm', 'stock': 9, 'featured': True, 'best_seller': True, 'new_arrival': False, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': 'executive-office-desk', 'seo_title': 'Executive Office Desk | Eagle Furniture Ngara', 'seo_description': 'Executive Office Desk from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0},

    {'id': 20, 'sku': 'OFF002', 'name': 'Ergonomic Office Chair', 'category': 'Office Furniture', 'subcategory': 'Office Chairs', 'price': 9000, 'sale_price': 6500, 'image': 'images/products/office-chair.jpg', 'gallery': ['images/products/office-chair.jpg'], 'description': 'Comfortable ergonomic chair with adjustable height and lumbar support.', 'material': 'Mesh & Steel', 'colour': 'Black', 'size': 'Standard', 'rating': 4.8, 'reviews': 41, 'stock': 15, 'featured': True, 'best_seller': True, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': 'ergonomic-office-chair', 'seo_title': 'Ergonomic Office Chair | Eagle Furniture Ngara', 'seo_description': 'Ergonomic Office Chair from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.'},

    {'id': 21, 'sku': 'MAT001', 'name': '6x6 Orthopedic Mattress', 'category': 'Mattresses', 'subcategory': 'Orthopedic Mattresses', 'price': 16000, 'image': 'images/categories/mattressess.jpg', 'gallery': ['images/categories/mattressess.jpg'], 'description': 'Premium orthopedic mattress offering excellent back support.', 'material': 'High Density Foam', 'colour': 'White', 'size': '6x6', 'rating': 4.9, 'reviews': 37, 'stock': 12, 'featured': True, 'best_seller': True, 'new_arrival': False, 'delivery': 'Nationwide', 'warranty': '5 Years', 'slug': '6x6-orthopedic-mattress', 'seo_title': '6x6 Orthopedic Mattress | Eagle Furniture Ngara', 'seo_description': '6x6 Orthopedic Mattress from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'sale_price': None},

    {'id': 22, 'sku': 'MAT002', 'name': '5x6 Spring Mattress', 'category': 'Mattresses', 'subcategory': 'Spring Mattresses', 'price': 15000, 'sale_price': 12000, 'image': 'images/categories/mattressess.jpg', 'gallery': ['images/categories/mattressess.jpg'], 'description': 'Comfortable spring mattress designed for everyday use.', 'material': 'Spring Foam', 'colour': 'White', 'size': '5x6', 'stock': 18, 'featured': False, 'best_seller': True, 'new_arrival': False, 'delivery': 'Nationwide', 'warranty': '5 Years', 'slug': '5x6-spring-mattress', 'seo_title': '5x6 Spring Mattress | Eagle Furniture Ngara', 'seo_description': '5x6 Spring Mattress from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0},

    {'id': 23, 'sku': 'OUT001', 'name': 'Outdoor Patio Set', 'category': 'Outdoor Furniture', 'subcategory': 'Outdoor Patio Sets', 'price': 58000, 'sale_price': 55000, 'image': 'images/categories/outdoor.jpg', 'gallery': ['images/categories/outdoor.jpg'], 'description': 'Weather-resistant patio set perfect for gardens and balconies.', 'material': 'Rattan', 'colour': 'Grey', 'size': '4 Seater', 'rating': 4.8, 'reviews': 18, 'stock': 6, 'featured': True, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': 'outdoor-patio-set', 'seo_title': 'Outdoor Patio Set | Eagle Furniture Ngara', 'seo_description': 'Outdoor Patio Set from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.'},

    {'id': 24, 'sku': 'OUT002', 'name': 'Outdoor Swing Chair', 'category': 'Outdoor Furniture', 'subcategory': 'Outdoor Swing Chairs', 'price': 26000, 'sale_price': 24000, 'image': 'images/categories/outdoor.jpg', 'gallery': ['images/categories/outdoor.jpg'], 'description': 'Stylish hanging swing chair for indoor and outdoor relaxation.', 'material': 'Rattan & Steel', 'colour': 'Brown', 'size': 'Single', 'rating': 4.9, 'reviews': 16, 'stock': 7, 'featured': True, 'best_seller': True, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '2 Years', 'slug': 'outdoor-swing-chair', 'seo_title': 'Outdoor Swing Chair | Eagle Furniture Ngara', 'seo_description': 'Outdoor Swing Chair from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.'},

    {'id': 25, 'sku': 'ACC001', 'name': 'Decorative Wall Mirror', 'category': 'Home Accessories', 'subcategory': 'Wall Mirrors', 'price': 9500, 'sale_price': 8500, 'image': 'images/products/mirror.jpg', 'gallery': ['images/products/mirror.jpg'], 'description': 'Elegant decorative mirror that complements any room.', 'material': 'Glass & Wood', 'colour': 'Gold', 'size': '80 cm', 'stock': 20, 'featured': False, 'best_seller': True, 'new_arrival': True, 'delivery': 'Nationwide', 'warranty': '1 Year', 'slug': 'decorative-wall-mirror', 'seo_title': 'Decorative Wall Mirror | Eagle Furniture Ngara', 'seo_description': 'Decorative Wall Mirror from Eagle Furniture Ngara. Custom furniture made to suit your space, with delivery available nationwide.', 'rating': None, 'reviews': 0},
    {'id': 31, 'sku': 'RST001', 'name': 'Custom Restaurant Dining Table', 'category': 'Restaurant Furniture', 'subcategory': 'Restaurant Tables', 'price': 35000, 'sale_price': 32000, 'image': None, 'gallery': [], 'description': 'Custom restaurant dining table designed for restaurants, cafés and hospitality spaces.', 'material': 'Hardwood', 'colour': 'Custom Colours', 'size': 'Custom', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'custom-restaurant-dining-table', 'seo_title': 'Custom Restaurant Dining Table | Eagle Furniture Ngara', 'seo_description': 'Custom restaurant dining tables from Eagle Furniture Ngara in Nairobi for restaurants, cafés and hospitality spaces.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 32, 'sku': 'RST002', 'name': 'Commercial Restaurant Chairs', 'category': 'Restaurant Furniture', 'subcategory': 'Restaurant Chairs', 'price': 6500, 'sale_price': 5800, 'image': None, 'gallery': [], 'description': 'Durable commercial restaurant chairs designed for restaurants, cafés, hotels and hospitality spaces.', 'material': 'Hardwood', 'colour': 'Custom Colours', 'size': 'Standard', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'commercial-restaurant-chairs', 'seo_title': 'Commercial Restaurant Chairs | Eagle Furniture Ngara', 'seo_description': 'Commercial restaurant chairs from Eagle Furniture Ngara in Nairobi for restaurants, cafés and hotels.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 33, 'sku': 'RST003', 'name': 'Custom Restaurant Booth Seating', 'category': 'Restaurant Furniture', 'subcategory': 'Restaurant Booths', 'price': 45000, 'sale_price': 42000, 'image': None, 'gallery': [], 'description': 'Custom restaurant booth seating designed for comfort, space efficiency and hospitality interiors.', 'material': 'Hardwood & Upholstery', 'fabric': 'Premium Fabric', 'colour': 'Custom Colours', 'size': 'Custom', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'custom-restaurant-booth-seating', 'seo_title': 'Custom Restaurant Booth Seating | Eagle Furniture Ngara', 'seo_description': 'Custom restaurant booth seating in Nairobi by Eagle Furniture Ngara for restaurants, cafés and hospitality spaces.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 34, 'sku': 'RST004', 'name': 'Commercial Bar Stools', 'category': 'Restaurant Furniture', 'subcategory': 'Bar Furniture', 'price': 8500, 'sale_price': 7500, 'image': None, 'gallery': [], 'description': 'Commercial bar stools suitable for restaurants, bars, cafés and hotels.', 'material': 'Hardwood & Metal', 'colour': 'Custom Colours', 'size': 'Standard', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'commercial-bar-stools', 'seo_title': 'Commercial Bar Stools | Eagle Furniture Ngara', 'seo_description': 'Commercial bar stools from Eagle Furniture Ngara in Nairobi for bars, restaurants and cafés.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 35, 'sku': 'RST005', 'name': 'Outdoor Restaurant Dining Set', 'category': 'Restaurant Furniture', 'subcategory': 'Outdoor Restaurant Furniture', 'price': 55000, 'sale_price': 52000, 'image': None, 'gallery': [], 'description': 'Outdoor restaurant dining set designed for cafés, restaurants, hotels and hospitality spaces.', 'material': 'Weather-Resistant Materials', 'colour': 'Custom Colours', 'size': 'Custom', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'outdoor-restaurant-dining-set', 'seo_title': 'Outdoor Restaurant Dining Set | Eagle Furniture Ngara', 'seo_description': 'Outdoor restaurant dining sets from Eagle Furniture Ngara in Nairobi for restaurants and hospitality spaces.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 36, 'sku': 'SCH001', 'name': 'Two-Seater Student Desk', 'category': 'School Furniture', 'subcategory': 'Student Desks', 'price': 7500, 'sale_price': 7000, 'image': None, 'gallery': [], 'description': 'Durable two-seater student desk designed for schools, academies and learning institutions.', 'material': 'Hardwood & MDF', 'colour': 'Custom Finish', 'size': 'Two Seater', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'two-seater-student-desk', 'seo_title': 'Two-Seater Student Desk | Eagle Furniture Ngara', 'seo_description': 'Two-seater student desks from Eagle Furniture Ngara in Nairobi for schools and learning institutions.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 37, 'sku': 'SCH002', 'name': 'School Student Chair', 'category': 'School Furniture', 'subcategory': 'Student Chairs', 'price': 3500, 'sale_price': 3200, 'image': None, 'gallery': [], 'description': 'Strong and practical student chair designed for classrooms and educational institutions.', 'material': 'Hardwood', 'colour': 'Custom Finish', 'size': 'Standard', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'school-student-chair', 'seo_title': 'School Student Chair | Eagle Furniture Ngara', 'seo_description': 'School student chairs from Eagle Furniture Ngara in Nairobi for classrooms and schools.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 38, 'sku': 'SCH003', 'name': 'Teachers Office Desk', 'category': 'School Furniture', 'subcategory': 'Teachers Desks', 'price': 22000, 'sale_price': 20000, 'image': None, 'gallery': [], 'description': 'Practical teachers office desk designed for classrooms, staff rooms and school offices.', 'material': 'MDF & Hardwood', 'colour': 'Custom Finish', 'size': 'Standard', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'teachers-office-desk', 'seo_title': 'Teachers Office Desk | Eagle Furniture Ngara', 'seo_description': 'Teachers office desks from Eagle Furniture Ngara in Nairobi for schools and staff offices.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 39, 'sku': 'SCH004', 'name': 'Classroom Tables', 'category': 'School Furniture', 'subcategory': 'School Tables', 'price': 12000, 'sale_price': 11000, 'image': None, 'gallery': [], 'description': 'Durable classroom tables suitable for schools, colleges, academies and training institutions.', 'material': 'Hardwood & MDF', 'colour': 'Custom Finish', 'size': 'Custom', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'classroom-tables', 'seo_title': 'Classroom Tables | Eagle Furniture Ngara', 'seo_description': 'Classroom tables from Eagle Furniture Ngara in Nairobi for schools and learning institutions.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 40, 'sku': 'SCH005', 'name': 'School Storage Cabinet', 'category': 'School Furniture', 'subcategory': 'School Storage', 'price': 28000, 'sale_price': 25000, 'image': None, 'gallery': [], 'description': 'School storage cabinet designed for books, learning materials, files and classroom supplies.', 'material': 'MDF & Hardwood', 'colour': 'Custom Finish', 'size': 'Custom', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'school-storage-cabinet', 'seo_title': 'School Storage Cabinet | Eagle Furniture Ngara', 'seo_description': 'School storage cabinets from Eagle Furniture Ngara in Nairobi for schools and learning institutions.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 41, 'sku': 'HOM001', 'name': 'Modern Home Wall Unit', 'category': 'Home Furniture', 'subcategory': 'Wall Units', 'price': 65000, 'sale_price': 60000, 'image': None, 'gallery': [], 'description': 'Modern custom wall unit combining TV space, display shelves and practical storage.', 'material': 'MDF & Hardwood', 'colour': 'Custom Finish', 'size': 'Custom', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'modern-home-wall-unit', 'seo_title': 'Modern Home Wall Unit | Eagle Furniture Ngara', 'seo_description': 'Modern home wall units from Eagle Furniture Ngara in Nairobi, custom-made for your space.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 42, 'sku': 'HOM002', 'name': 'Modern Console Table', 'category': 'Home Furniture', 'subcategory': 'Console Tables', 'price': 18000, 'sale_price': 16000, 'image': None, 'gallery': [], 'description': 'Modern console table suitable for entryways, living rooms, hallways and decorative interiors.', 'material': 'Hardwood', 'colour': 'Custom Finish', 'size': 'Standard', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'modern-console-table', 'seo_title': 'Modern Console Table | Eagle Furniture Ngara', 'seo_description': 'Modern console tables from Eagle Furniture Ngara in Nairobi for contemporary homes.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 43, 'sku': 'HOM003', 'name': 'Wooden Side Table', 'category': 'Home Furniture', 'subcategory': 'Side Tables', 'price': 9500, 'sale_price': 8500, 'image': None, 'gallery': [], 'description': 'Practical wooden side table designed to complement sofas, beds, lounge areas and modern interiors.', 'material': 'Hardwood', 'colour': 'Custom Finish', 'size': 'Standard', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'wooden-side-table', 'seo_title': 'Wooden Side Table | Eagle Furniture Ngara', 'seo_description': 'Wooden side tables from Eagle Furniture Ngara in Nairobi for living rooms and bedrooms.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 44, 'sku': 'HOM004', 'name': 'Custom Wooden Bench', 'category': 'Home Furniture', 'subcategory': 'Benches', 'price': 14000, 'sale_price': 12500, 'image': None, 'gallery': [], 'description': 'Custom wooden bench suitable for entryways, bedrooms, dining spaces and home interiors.', 'material': 'Hardwood', 'colour': 'Custom Finish', 'size': 'Custom', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'custom-wooden-bench', 'seo_title': 'Custom Wooden Bench | Eagle Furniture Ngara', 'seo_description': 'Custom wooden benches from Eagle Furniture Ngara in Nairobi for homes and interiors.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 45, 'sku': 'HOM005', 'name': 'Home Storage Cabinet', 'category': 'Home Furniture', 'subcategory': 'Home Storage', 'price': 30000, 'sale_price': 27500, 'image': None, 'gallery': [], 'description': 'Practical home storage cabinet designed to keep living spaces organised.', 'material': 'MDF & Hardwood', 'colour': 'Custom Finish', 'size': 'Custom', 'stock': 0, 'featured': False, 'best_seller': False, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'home-storage-cabinet', 'seo_title': 'Home Storage Cabinet | Eagle Furniture Ngara', 'seo_description': 'Home storage cabinets from Eagle Furniture Ngara in Nairobi, custom-made for your space.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 46, 'sku': 'PKG001', 'name': 'Living Room Furniture Package', 'category': 'Full Package Furniture', 'subcategory': 'Living Room Package', 'price': 150000, 'sale_price': 140000, 'image': None, 'gallery': [], 'description': 'Complete living room furniture package designed for a coordinated, comfortable and stylish living space.', 'material': 'Custom Materials', 'colour': 'Custom Colours', 'size': 'Custom', 'stock': 0, 'featured': True, 'best_seller': True, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'living-room-furniture-package', 'seo_title': 'Living Room Furniture Package | Eagle Furniture Ngara', 'seo_description': 'Living room furniture package from Eagle Furniture Ngara in Nairobi for a coordinated custom living space.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 47, 'sku': 'PKG002', 'name': 'Bedroom Furniture Package', 'category': 'Full Package Furniture', 'subcategory': 'Bedroom Package', 'price': 140000, 'sale_price': 130000, 'image': None, 'gallery': [], 'description': 'Complete bedroom furniture package designed for a coordinated and functional bedroom setup.', 'material': 'Custom Materials', 'colour': 'Custom Colours', 'size': 'Custom', 'stock': 0, 'featured': True, 'best_seller': True, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'bedroom-furniture-package', 'seo_title': 'Bedroom Furniture Package | Eagle Furniture Ngara', 'seo_description': 'Bedroom furniture package from Eagle Furniture Ngara in Nairobi for a coordinated custom bedroom.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 48, 'sku': 'PKG003', 'name': 'Dining Furniture Package', 'category': 'Full Package Furniture', 'subcategory': 'Dining Package', 'price': 95000, 'sale_price': 88000, 'image': 'images/products/dining-set.jpg', 'gallery': ['images/products/dining-set.jpg'], 'description': 'Complete dining furniture package designed for a coordinated and stylish dining area.', 'material': 'Hardwood', 'colour': 'Custom Finish', 'size': 'Custom', 'stock': 0, 'featured': True, 'best_seller': True, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'dining-furniture-package', 'seo_title': 'Dining Furniture Package | Eagle Furniture Ngara', 'seo_description': 'Dining furniture package from Eagle Furniture Ngara in Nairobi for a complete coordinated dining space.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 49, 'sku': 'PKG004', 'name': 'Complete Home Furniture Package', 'category': 'Full Package Furniture', 'subcategory': 'Complete Home Package', 'price': 350000, 'sale_price': 325000, 'image': None, 'gallery': [], 'description': 'Complete home furniture package designed to furnish multiple rooms with coordinated custom-made furniture.', 'material': 'Custom Materials', 'colour': 'Custom Colours', 'size': 'Custom', 'stock': 0, 'featured': True, 'best_seller': True, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'complete-home-furniture-package', 'seo_title': 'Complete Home Furniture Package | Eagle Furniture Ngara', 'seo_description': 'Complete home furniture package from Eagle Furniture Ngara in Nairobi for coordinated bespoke furniture.', 'rating': None, 'reviews': 0, 'warranty': None},
    {'id': 50, 'sku': 'PKG005', 'name': 'Complete Office Furniture Package', 'category': 'Full Package Furniture', 'subcategory': 'Office Package', 'price': 180000, 'sale_price': 165000, 'image': None, 'gallery': [], 'description': 'Complete office furniture package designed for professional, functional and coordinated workspaces.', 'material': 'Custom Materials', 'colour': 'Custom Colours', 'size': 'Custom', 'stock': 0, 'featured': True, 'best_seller': True, 'new_arrival': True, 'delivery': 'Nationwide', 'slug': 'complete-office-furniture-package', 'seo_title': 'Complete Office Furniture Package | Eagle Furniture Ngara', 'seo_description': 'Complete office furniture package from Eagle Furniture Ngara in Nairobi for professional workspaces.', 'rating': None, 'reviews': 0, 'warranty': None},
]


# ---------------------------------------------------------------------------
# Catalogue helpers
# ---------------------------------------------------------------------------

def get_all_products() -> list[dict]:
    """Return every product in the master catalogue."""
    return products


def get_product_by_id(product_id: int | str) -> Optional[dict]:
    """Find one product by numeric catalogue ID."""
    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return None

    return next((p for p in products if p.get("id") == product_id), None)


def get_product_by_sku(sku: str) -> Optional[dict]:
    """Find one product by SKU, case-insensitively."""
    if not sku:
        return None

    sku = str(sku).strip().upper()
    return next(
        (p for p in products if str(p.get("sku", "")).upper() == sku),
        None,
    )


def get_product_by_slug(slug: str) -> Optional[dict]:
    """Find one product by SEO slug."""
    if not slug:
        return None

    slug = slugify(slug)
    return next((p for p in products if p.get("slug") == slug), None)


def get_featured_products() -> list[dict]:
    return [p for p in products if p.get("featured")]


def get_best_sellers() -> list[dict]:
    return [p for p in products if p.get("best_seller")]


def get_new_arrivals() -> list[dict]:
    return [p for p in products if p.get("new_arrival")]


def get_sale_products() -> list[dict]:
    return [
        p for p in products
        if p.get("sale_price") is not None
        and p.get("price") is not None
        and p["sale_price"] < p["price"]
    ]


def get_products_by_category(category: str) -> list[dict]:
    if not category:
        return []

    target = str(category).strip().lower()
    return [
        p for p in products
        if str(p.get("category", "")).strip().lower() == target
    ]


def get_products_by_subcategory(subcategory: str) -> list[dict]:
    if not subcategory:
        return []

    target = str(subcategory).strip().lower()
    return [
        p for p in products
        if str(p.get("subcategory", "")).strip().lower() == target
    ]


def get_products_by_category_and_subcategory(
    category: str,
    subcategory: str,
) -> list[dict]:
    if not category or not subcategory:
        return []

    category_target = str(category).strip().lower()
    subcategory_target = str(subcategory).strip().lower()

    return [
        p for p in products
        if str(p.get("category", "")).strip().lower() == category_target
        and str(p.get("subcategory", "")).strip().lower() == subcategory_target
    ]


def search_products(query: str) -> list[dict]:
    """Search name, SKU, category, subcategory and description."""
    if not query:
        return products

    query = str(query).strip().lower()
    if not query:
        return products

    fields = (
        "name",
        "sku",
        "category",
        "subcategory",
        "description",
        "material",
        "colour",
        "size",
    )

    return [
        p for p in products
        if any(query in str(p.get(field, "")).lower() for field in fields)
    ]


def get_effective_price(product: dict) -> Optional[float]:
    """Return sale price when active, otherwise regular price."""
    sale = product.get("sale_price")
    price = product.get("price")

    if sale is not None and price is not None and sale < price:
        return sale

    return price


def get_related_products(product: dict, limit: int = 8) -> list[dict]:
    """
    Return related products from the same subcategory first,
    then the same category.
    """
    if not product:
        return []

    product_id = product.get("id")
    category = str(product.get("category", "")).strip().lower()
    subcategory = str(product.get("subcategory", "")).strip().lower()

    related = [
        p for p in products
        if p.get("id") != product_id
        and str(p.get("subcategory", "")).strip().lower() == subcategory
    ]

    if len(related) < limit:
        related_ids = {p.get("id") for p in related}
        related.extend(
            p for p in products
            if p.get("id") != product_id
            and p.get("id") not in related_ids
            and str(p.get("category", "")).strip().lower() == category
        )

    return related[:limit]


def get_categories() -> list[str]:
    """Return unique catalogue categories in catalogue order."""
    seen = set()
    result = []

    for product in products:
        category = product.get("category")
        if category and category not in seen:
            seen.add(category)
            result.append(category)

    return result


def get_subcategories(category: str | None = None) -> list[str]:
    """Return unique subcategories, optionally limited to one category."""
    source = products if not category else get_products_by_category(category)

    seen = set()
    result = []

    for product in source:
        subcategory = product.get("subcategory")
        if subcategory and subcategory not in seen:
            seen.add(subcategory)
            result.append(subcategory)

    return result


def validate_catalogue() -> list[str]:
    """
    Validate the catalogue for common importer problems.

    Returns a list of error messages. An empty list means no validation
    errors were found.
    """
    errors = []
    ids = set()
    skus = set()
    slugs = set()

    required = (
        "id",
        "sku",
        "name",
        "category",
        "subcategory",
        "price",
        "description",
    )

    for index, product in enumerate(products, start=1):
        prefix = f"Product #{index}"

        for field in required:
            if not product.get(field):
                errors.append(f"{prefix}: missing '{field}'")

        product_id = product.get("id")
        if product_id in ids:
            errors.append(f"{prefix}: duplicate id '{product_id}'")
        ids.add(product_id)

        sku = str(product.get("sku", "")).upper()
        if sku in skus:
            errors.append(f"{prefix}: duplicate SKU '{sku}'")
        skus.add(sku)

        slug = product.get("slug") or slugify(product.get("name", ""))
        if slug in slugs:
            errors.append(f"{prefix}: duplicate slug '{slug}'")
        slugs.add(slug)

        price = product.get("price")
        sale_price = product.get("sale_price")

        if price is not None and price < 0:
            errors.append(f"{prefix}: negative price")

        if sale_price is not None and sale_price < 0:
            errors.append(f"{prefix}: negative sale price")

        if (
            price is not None
            and sale_price is not None
            and sale_price >= price
        ):
            errors.append(
                f"{prefix}: sale_price must be lower than price"
            )

        # Gallery images are optional until verified product photography is available.

    return errors


CATALOGUE_SUMMARY = {
    "total_products": len(products),
    "categories": get_categories(),
    "subcategories": get_subcategories(),
}


__all__ = [
    "products",
    "slugify",
    "get_all_products",
    "get_product_by_id",
    "get_product_by_sku",
    "get_product_by_slug",
    "get_featured_products",
    "get_best_sellers",
    "get_new_arrivals",
    "get_sale_products",
    "get_products_by_category",
    "get_products_by_subcategory",
    "get_products_by_category_and_subcategory",
    "search_products",
    "get_effective_price",
    "get_related_products",
    "get_categories",
    "get_subcategories",
    "validate_catalogue",
    "CATALOGUE_SUMMARY",
]
