from typing import List

from tinyshop.domain.Money import Money
from tinyshop.domain.Product import Product
from tinyshop.repositories.protocols import ProductRepository


class ProductService:

    def __init__(self,repo:ProductRepository) -> None:

        self.repo = repo


    def create_product(self,product_id:int,title:str,currency:str,amount:int) -> Product:
        money = Money(amount=amount,currency=currency)
        product = Product(id=product_id,title=title,price=money)
        self.repo.add(product)
        return product

    def apply_discount(self,percent:int,product_id:int) -> Product:
        product = self.repo.get(product_id=product_id)
        discounted_product = product.apply_discount(percent)
        self.repo.remove(product_id=product_id)
        self.repo.add(discounted_product)
        return discounted_product
    def list_products(self) -> List[Product]:
        products = self.repo.list()
        return list(products)
    def get_product_by_id(self,product_id:int) -> Product:
        product = self.repo.get(product_id=product_id)
        return product
    def remove_product(self,product_id:int) -> None:
        self.repo.remove(product_id=product_id)
    def search_products(self, query:str) -> List[Product]:
        products = self.list_products()
        normalized_query = query.strip().lower()
        if len(normalized_query) == 0:
            return products
        results = [product for product in products if normalized_query in product.title.lower()]
        return results