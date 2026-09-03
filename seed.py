from app import create_app
from app.seeds.seed_categories import seed_categories
from app.seeds.seed_products import seed_products

app = create_app()

with app.app_context():

    seed_categories()

    seed_products()

    print("Database seeding completed.")