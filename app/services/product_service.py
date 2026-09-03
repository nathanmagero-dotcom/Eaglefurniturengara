from app.models.product import Product


class ProductService:

    @staticmethod
    def all():
        return Product.query.order_by(Product.name).all()

    @staticmethod
    def featured():
        return Product.query.filter_by(featured=True).all()

    @staticmethod
    def best_sellers():
        return Product.query.filter_by(best_seller=True).all()

    @staticmethod
    def new_arrivals():
        return Product.query.filter_by(new_arrival=True).all()

    @staticmethod
    def by_id(product_id):
        return Product.query.get_or_404(product_id)

    @staticmethod
    def by_category(category_id):
        return Product.query.filter_by(
            category_id=category_id
        ).all()

    @staticmethod
    def search(keyword):

        return Product.query.filter(

            Product.name.ilike(f"%{keyword}%")

        ).all()