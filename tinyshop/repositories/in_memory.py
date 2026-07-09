from pathlib import Path
from typing import Iterable

from tinyshop.domain.CartItem import Cart
from tinyshop.domain.Order import Order
from tinyshop.domain.Product import Product
from tinyshop.repositories.protocols import ProductRepository, CartRepository, OrderRepository


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
    def __init__(self) -> None:
        self._carts: dict[int, Cart] = {}
    def add(self ,cart: Cart) -> None:
        if cart.id   in self._carts:
            raise ValueError(f'Cart {cart} already exist')
        self._carts[cart.id] = cart
    def get(self, cart_id :int) -> Cart:
        try:
            return self._carts[cart_id]
        except KeyError:
            raise ValueError("Cart not found")
    def list(self) -> Iterable[Cart]:
        return self._carts.values()
    def remove(self ,cart_id :int) -> None:
        try:
            del self._carts[cart_id]
        except KeyError:
            raise ValueError("Cart not found")



class InMemoryOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}
    def add(self ,order :Order) -> None:
        if order.id in self._orders:
            raise ValueError(f'Order {order.id} already exists')
        self._orders[order.id] = order
    def get(self, order_id :int) -> Order:
        if order_id not in self._orders:
            raise ValueError("Order not found")
        return self._orders[order_id]
    def list(self) -> Iterable[Order]:
        return self._orders.values()
    def remove(self ,order_id :int) -> None:
        if order_id not in self._orders:
            raise ValueError("Order not found")
        del self._orders[order_id]