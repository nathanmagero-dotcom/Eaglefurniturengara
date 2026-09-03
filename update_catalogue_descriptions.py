from app import create_app
from app.extensions import db
from app.models.product import Product

app = create_app()

descriptions = {
    "6 Seater L-Shaped Sofa":
        "Modern 6-seater L-shaped sofa designed for spacious and comfortable family living. Built with a strong hardwood frame and high-density cushioning for excellent support and lasting comfort. The practical L-shaped design provides generous seating while making efficient use of your living-room space. Ideal for modern homes, apartments and family living rooms.",

    "5 Seater Modern Sofa":
        "Stylish 5-seater modern sofa designed to bring comfort and contemporary elegance to your living room. Its practical seating capacity makes it ideal for apartments, family homes and modern interiors. Perfect for everyday relaxation, entertaining guests and creating a comfortable living-room setup.",

    "7 Seater Luxury Sofa":
        "Spacious 7-seater luxury sofa designed for large and comfortable living rooms. Its generous seating provides plenty of room for family and guests while adding a premium and sophisticated look to your interior. Ideal for large family homes and contemporary living spaces.",

    "3 Seater Chesterfield Sofa":
        "Classic 3-seater Chesterfield sofa featuring an elegant button-tufted design. Its timeless appearance works beautifully in modern and traditional interiors while providing comfortable everyday seating. Suitable for living rooms, offices, reception areas and customers looking for a stylish statement sofa.",

    "Recliner Sofa Set":
        "Premium recliner sofa set designed for maximum relaxation and comfortable everyday living. The reclining design provides a relaxing seating experience for watching television, resting and spending time with family. An excellent choice for customers looking for a comfortable and premium living-room sofa set.",

    "Queen Size Bed":
        "Comfortable queen-size bed designed to provide a stylish and relaxing sleeping environment. Its practical size makes it ideal for couples and spacious bedrooms. A great choice for modern homes and customers looking for a durable, elegant bedroom centrepiece.",

    "King Size Bed":
        "Spacious king-size bed designed for superior sleeping comfort and a luxurious bedroom appearance. Ideal for couples who prefer generous sleeping space and a strong statement piece for their bedroom. Suitable for modern homes and spacious master bedrooms.",

    "4x6 Bed":
        "Practical 4x6 bed designed for comfortable everyday sleeping while making efficient use of bedroom space. A suitable choice for single sleepers, guest rooms and compact bedrooms. Combining functionality and a clean furniture design for modern homes.",

    "4 Seater Dining Set":
        "Elegant 4-seater dining set designed for comfortable family meals and everyday dining. Its compact configuration makes it ideal for apartments, smaller dining areas and modern homes. Perfect for enjoying meals with family while adding a stylish touch to your dining space.",

    "6 Seater Dining Set":
        "Spacious 6-seater dining set designed for comfortable family dining and entertaining guests. Provides practical seating for everyday meals while creating an attractive centrepiece for the dining room. Ideal for family homes and modern interiors.",

    "8 Seater Dining Set":
        "Luxury 8-seater dining set designed for spacious dining rooms and larger families. Provides generous seating for family meals and entertaining guests while giving your dining area a sophisticated appearance. Ideal for customers looking for a statement dining set.",

    "Modern TV Unit":
        "Modern TV unit designed to give your entertainment area a clean, stylish and organised appearance. Provides an attractive centrepiece for the living room while offering practical space for your television and entertainment accessories. Ideal for contemporary homes.",

    "Floating TV Unit":
        "Contemporary floating TV unit designed to create a sleek and modern entertainment area. Its wall-mounted style gives the living room a clean appearance while helping maximise available floor space. Ideal for modern apartments and stylish living rooms.",

    "Modern Coffee Table":
        "Stylish modern coffee table designed to complement contemporary living-room furniture. Its practical design provides a convenient surface for drinks, décor and everyday essentials while adding a polished finishing touch to your seating area.",

    "Luxury Marble Coffee Table":
        "Elegant luxury marble coffee table designed to add a sophisticated statement to your living room. Its premium-inspired appearance pairs beautifully with modern sofas and luxury interiors, providing both practical surface space and an attractive decorative centrepiece.",

    "2 Door Wardrobe":
        "Practical 2-door wardrobe designed to provide organised clothing and bedroom storage. Its compact design makes it suitable for bedrooms where efficient use of space is important. A functional choice for modern homes, apartments and guest bedrooms.",

    "3 Door Wardrobe":
        "Spacious 3-door wardrobe designed to provide convenient clothing and bedroom storage. Its larger storage capacity makes it suitable for family bedrooms and customers who need additional wardrobe space. Combines practical organisation with a clean modern appearance.",

    "Sliding Door Wardrobe":
        "Modern sliding-door wardrobe designed for stylish and space-efficient bedroom storage. The sliding door system makes it practical for bedrooms with limited floor space while providing generous storage for clothing and personal belongings.",

    "Executive Office Desk":
        "Professional executive office desk designed for productive and organised workspaces. Its substantial design provides a practical working surface for office tasks, documents and equipment. Suitable for offices, executive workspaces and professional environments.",

    "Ergonomic Office Chair":
        "Ergonomic office chair designed to provide comfortable seating during long working hours. Its supportive design is suitable for offices, home workspaces and professional environments where comfort and productivity matter.",

    "6x6 Orthopedic Mattress":
        "6x6 orthopedic mattress designed to provide supportive and comfortable sleep. A practical choice for customers looking for enhanced sleeping support and a spacious mattress size for a master bedroom.",

    "5x6 Spring Mattress":
        "5x6 spring mattress designed to provide comfortable everyday sleeping support. Its practical size makes it suitable for bedrooms where dependable comfort and value are important.",

    "Outdoor Patio Set":
        "Outdoor patio furniture set designed for comfortable outdoor relaxation and entertaining. Ideal for patios, balconies, gardens and outdoor living areas where you want practical seating combined with an attractive furniture setup.",

    "Outdoor Swing Chair":
        "Stylish outdoor swing chair designed for relaxing and enjoying your outdoor space. Ideal for patios, balconies, gardens and leisure areas where you want a comfortable and attractive seating option.",

    "Decorative Wall Mirror":
        "Elegant decorative wall mirror designed to enhance bedrooms, living rooms, hallways and other interior spaces. A stylish décor piece that can brighten a room and complement modern furniture arrangements.",

    "Custom Restaurant Dining Table":
        "Commercial restaurant dining table designed for restaurants, cafés and hospitality spaces. Suitable for businesses looking for practical dining furniture with a professional appearance. Custom furniture options can be considered based on your space and requirements.",

    "Commercial Restaurant Chairs":
        "Durable commercial restaurant chairs designed for restaurants, cafés and hospitality environments. Practical for everyday customer use while providing a clean and professional appearance for dining spaces.",

    "Custom Restaurant Booth Seating":
        "Custom restaurant booth seating designed for restaurants, cafés and hospitality spaces. Provides comfortable customer seating while helping businesses create an attractive and efficient dining layout. Custom configurations can be made to suit the available space.",

    "Commercial Bar Stools":
        "Commercial bar stools designed for restaurants, cafés, bars and kitchen counter areas. A practical seating solution for hospitality businesses looking for functional and attractive commercial furniture.",

    "Outdoor Restaurant Dining Set":
        "Outdoor restaurant dining set designed for cafés, restaurants and hospitality businesses with outdoor seating areas. Provides a practical furniture solution for outdoor customer dining and entertaining.",

    "Two-Seater Student Desk":
        "Two-seater student desk designed for schools, learning institutions and classrooms. Provides practical workspace for two students while supporting an organised and efficient classroom environment.",

    "School Student Chair":
        "School student chair designed for classrooms, schools and learning institutions. Provides practical seating for students and is suitable for everyday educational environments.",

    "Teachers Office Desk":
        "Teachers office desk designed for classrooms, staffrooms and school administration spaces. Provides a practical working surface for teachers and school staff while maintaining an organised professional workspace.",

    "Classroom Tables":
        "Classroom tables designed for schools, training centres and learning institutions. Suitable for student activities, group learning and classroom arrangements requiring practical and functional work surfaces.",

    "School Storage Cabinet":
        "School storage cabinet designed to help schools and learning institutions organise books, teaching materials, files and classroom supplies. A practical storage solution for classrooms, offices and staff areas.",

    "Modern Home Wall Unit":
        "Modern home wall unit designed to create an attractive and organised living-room entertainment area. Provides a stylish focal point for your television and décor while helping organise the space around your entertainment setup.",

    "Modern Console Table":
        "Modern console table designed to add style and practical surface space to entryways, living rooms, hallways and other interior areas. Ideal for displaying décor, mirrors, accessories and everyday essentials.",

    "Wooden Side Table":
        "Practical wooden side table designed to complement sofas, beds and other furniture. Suitable for placing drinks, décor, lamps and everyday essentials while adding a warm furniture accent to your interior.",

    "Custom Wooden Bench":
        "Custom wooden bench designed for practical seating in homes, entryways, dining areas and other interior spaces. A versatile furniture piece that can be customised to suit different spaces and requirements.",

    "Home Storage Cabinet":
        "Practical home storage cabinet designed to help organise household items while keeping living spaces neat and attractive. Suitable for bedrooms, living rooms, offices and other areas requiring additional storage.",

    "Living Room Furniture Package":
        "Complete living room furniture package designed to help you create a coordinated and stylish living space. A convenient option for customers looking for matching furniture pieces for a complete living-room setup.",

    "Bedroom Furniture Package":
        "Bedroom furniture package designed to create a coordinated and comfortable bedroom setup. A convenient option for customers looking for matching bedroom furniture while saving time when furnishing their space.",

    "Dining Furniture Package":
        "Dining furniture package designed to create a complete and coordinated dining area. Ideal for customers looking for a convenient furniture solution for family dining and entertaining.",

    "Complete Home Furniture Package":
        "Complete home furniture package designed for customers furnishing an entire home. Provides a convenient way to coordinate furniture across key living spaces while creating a consistent and comfortable interior.",

    "Complete Office Furniture Package":
        "Complete office furniture package designed to help businesses create an organised and professional workspace. Suitable for offices requiring coordinated desks, chairs and other essential furniture for productive working environments."
}

with app.app_context():
    updated = 0

    for name, description in descriptions.items():
        product = Product.query.filter_by(name=name).first()

        if product:
            product.description = description
            updated += 1

    db.session.commit()

    print()
    print("=" * 70)
    print(f"UPDATED PRODUCTS: {updated}")
    print("=" * 70)