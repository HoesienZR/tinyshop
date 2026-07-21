from abc import ABC, abstractmethod

from tinyshop.domain.cart_Item import Cart
from tinyshop.domain.order import Order
from tinyshop.repositories.protocols import CartRepository,OrderRepository
from tinyshop.application.storage import MemoryStorage
class AbstractUnitOfWork(ABC):
    carts: CartRepository
    orders:  OrderRepository

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else :
            self.rollback()
    @abstractmethod
    def rollback(self): ...
    @abstractmethod
    def commit(self): ...

class InMemoryUnitOfWork(AbstractUnitOfWork):
    def __init__(self,carts_repository: CartRepository,orders_repository:OrderRepository,in_memory_storage:MemoryStorage)-> None :
        self.carts = carts_repository
        self.orders = orders_repository
        self._session  = Session(in_memory_storage)

        self._committed = False
        
    def rollback(self) -> None :
        self._session.clear()
        self._committed = False
    def commit(self)-> None :
        orders = self._session.new_orders
        carts = self._session.new_carts
        for order_id,order in orders.items():
            self._session.storage.add_order(order=order)
        for cart_id,cart  in carts.items():
            self._session.storage.add_cart(cart=cart)
        self._session.clear()
        self._committed = True
    @property
    def session(self) -> "Session" :
        return self._session

class Session:
    def __init__(self,storage:MemoryStorage) -> None:
        self.new_orders:dict[int, Order] = {}
        self.new_carts:dict[int , Cart] = {}
        self.storage = storage
    def add_new_order(self, order: Order) -> None :
        self.new_orders.update({order.id:order})
    def add_carts(self, cart:Cart) -> None :
        self.new_carts.update({cart.id:cart})
    def clear(self)-> None :
        self.new_orders.clear()
        self.new_carts.clear()
    def get_order(self, order_id:int) -> Order:
        order = self.new_orders.get(order_id, None)
        if order is None:
            order = self.storage.get_order(order_id)
            if order is None:
                raise ValueError(f"Order {order_id} not found")
        return order
    def get_cart(self, cart_id:int) -> Cart:
        cart = self.new_carts.get(cart_id, None)
        if cart is None:
            cart = self.storage.get_cart(cart_id)
            if cart is None:
                raise ValueError(f"Cart {cart_id} not found")
        return cart




