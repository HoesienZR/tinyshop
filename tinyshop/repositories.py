import json
from typing import Iterable, Protocol
from pathlib import Path

from tinyshop.domain import Order
from tinyshop.domain.models import Product, Cart


class ProductRepository(Protocol):
    def add(self, product: Product) -> None: ...

    def get(self, product_id: int) -> Product: ...

    def list(self) -> Iterable[Product]: ...

    def remove(self, product_id: int) -> None: ...


class InMemoryProductRepository(ProductRepository):
    def __init__(self) -> None:
        self._products: dict[int, Product] = {}

    def add(self,product: Product) -> None:
        if product.id  in self._products:
            raise ValueError(f'Product {product.id} already exists')
        self._products[product.id] = product

    def remove(self,product_id: int) -> None:
        if product_id  not in self._products:
            raise ValueError(f'Product {product_id} does not exist')
        del self._products[product_id]
    def list(self)->Iterable[Product]:
        return self._products.values()
    def get(self, product_id:int) -> Product:
        try:
            return self._products[product_id]
        except KeyError:
            raise ValueError("Product not found")

class JsonProductRepository(ProductRepository):
    def __init__(self,path:Path) -> None:
        self._file = Path(path)
        self._products = self._load()


    def _load(self) -> dict[int, Product]:
        if not self._file.exists():
            return {}
        try :
            with open(self._file,'r') as f:
                data = json.load(f)
            return {
                int(pid):Product.from_dict(product) for pid, product in data.items()
            }
        except (json.JSONDecodeError, ValueError):
            return {}
    def _save(self)-> None:
        with open(self._file,'w') as f:
            json.dump({
                pid:product.to_dict()
                for pid,product in self._products.items()
                },
            f,
            indent=4)
    def add(self,product: Product) -> None:
        if   product.id   in self._products:
            raise ValueError(f'Product {product.id} already exists')
        self._products[product.id] = product
        self._save()
    def get(self, product_id:int) -> Product:
        try:
            return self._products[product_id]
        except KeyError:
            raise ValueError("Product not found")
    def remove(self, product_id:int) -> None:
        if product_id not in self._products:
            raise ValueError("Product not found")
        del self._products[product_id]
        self._save()
    def list(self)->Iterable[Product]:
        return self._products.values()


class CartRepository(Protocol):
    def add(self,cart:Cart) -> None: ...
    def get(self, cart_id:int) -> Cart: ...
    def list(self) -> Iterable[Cart]: ...
    def remove(self,cart_id:int) -> None:...

class CartInMemoryRepository(CartRepository):
    def __init__(self) -> None:
        self._carts: dict[int, Cart] = {}
    def add(self,cart: Cart) -> None:
        if cart.id   in self._carts:
            raise ValueError(f'Cart {cart} already exist')
        self._carts[cart.id] = cart
    def get(self, cart_id:int) -> Cart:
        try:
            return self._carts[cart_id]
        except KeyError:
            raise ValueError("Cart not found")
    def list(self) -> Iterable[Cart]:
        return self._carts.values()
    def remove(self,cart_id:int) -> None:
        try:
            del self._carts[cart_id]
        except KeyError:
            raise ValueError("Cart not found")
class OrderRepository(Protocol):
    def add(self,order:Order) -> None: ...
    def get(self, order_id:int) -> Order: ...
    def list(self) -> Iterable[Order]: ...
    def remove(self,order_id:int) -> None:...
class InMemoryOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}
    def add(self,order:Order) -> None:
        if order.id in self._orders:
            raise ValueError(f'Order {order.id} already exists')
        self._orders[order.id] = order
    def get(self, order_id:int) -> Order:
        if order_id not in self._orders:
            raise ValueError("Order not found")
        return self._orders[order_id]
    def list(self) -> Iterable[Order]:
        return self._orders.values()
    def remove(self,order_id:int) -> None:
        if order_id not in self._orders:
            raise ValueError("Order not found")
        del self._orders[order_id]