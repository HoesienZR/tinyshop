from tinyshop.domain.Order import Order
from tinyshop.domain.Order import OrderItem
from tinyshop.domain.models import Product, Money, Cart
from typing import  List
from tinyshop.repositories import ProductRepository, CartRepository,OrderRepository


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
class CartService:
    def __init__(self,repo:CartRepository) -> None:
        self.repo = repo
    def create_cart(self,cart_id:int) -> Cart:
        cart =  Cart(id=cart_id)
        self.repo.add(cart)
        return cart
    def list_carts(self) -> List[Cart]:
        carts = self.repo.list()
        return list(carts)
    def remove_cart(self,cart_id:int) -> None:
        self.repo.remove(cart_id)
    def get_cart_by_id(self, cart_id:int) -> Cart:
        cart = self.repo.get(cart_id=cart_id)
        return cart
    def add_product_to_cart(self,product:Product,cart_id:int,quantity:int) -> Cart:
        cart = self.repo.get(cart_id=cart_id)
        cart.add_product(product=product,quantity=quantity)
        return cart
    def remove_product_from_cart(self,cart_id,product_id:int) ->Cart:
        #TODO this is based on domain not service we have to change this

        cart = self.repo.get(cart_id=cart_id)
        cart.remove_product(product_id=product_id)
        return cart
    def change_product_quantity(self,cart_id:int,product_id:int,change:int) -> Cart:
        # TODO this is based on domain not service we have to change this
        cart = self.repo.get(cart_id=cart_id)
        cart.change_quantity(product_id=product_id,change=change)
        return cart

class CheckoutService:
    def __init__(self,
                 cart_repository:CartRepository,
                 order_repository:OrderRepository) -> None:
        self.cart_repository = cart_repository
        self.order_repository = order_repository
    def checkout(self,cart_id:int,order_id) -> Order:
        cart = self.cart_repository.get(cart_id=cart_id)
        if not cart.items:
            raise ValueError(f"No items in  found in cart with item {cart_id}")
        order_items = []
        #TODO fix the type hint below
        for item in cart.items:
            order_items.append(OrderItem.from_cart_item(item))
        order = Order(id=order_id,items= tuple(order_items))
        self.order_repository.add(order=order)
        self.cart_repository.remove(cart_id=cart_id)
        return order

