from pathlib import Path
from typing import Iterable

from tinyshop.domain.product import Product
from tinyshop.domain.cart_Item import Cart
from tinyshop.domain.order import Order
from .protocols import ProductRepository, CartRepository, OrderRepository
from tinyshop.persistance import Session


class InMemoryProductRepository(ProductRepository):
    def __init__(self) -> None:
        self._products: dict[int, Product] = {}

    def add(self ,product: Product) -> None:
        if product.id  in self._products:
            raise ValueError(f'Product {product.id} already exists')
        self._products[product.id] = product

    def remove(self ,product_id: int) -> None:
        if product_id  not in self._products:
            raise ValueError(f'Product {product_id} does not exist')
        del self._products[product_id]
    def list(self )->Iterable[Product]:
        return self._products.values()
    def get(self, product_id :int) -> Product:
        try:
            return self._products[product_id]
        except KeyError:
            raise ValueError("Product not found")



class CartInMemoryRepository(CartRepository):
    def __init__(self,session:Session,) -> None:
        self.session = session
    def add(self ,cart: Cart) -> None:
        self.session.add_cart(cart)
    def get(self, cart_id :int) -> Cart:
        return self.session.get_cart(cart_id)
    def list(self) -> Iterable[Cart]:
        return self.session.cart_list()
    def remove(self ,cart_id :int) -> None:
        self.session.remove_cart(cart_id)



class InMemoryOrderRepository(OrderRepository):
    def __init__(self,session:Session) -> None:
        self.session = session
    def add(self ,order :Order) -> None:
        self.session.add_order(order)
    def get(self, order_id :int) -> Order:
        return self.session.get_order(order_id=order_id)
    def list(self) -> Iterable[Order]:
        return self.session.order_list()
    def remove(self ,order_id :int) -> None:
        self.session.remove_order(order_id=order_id)