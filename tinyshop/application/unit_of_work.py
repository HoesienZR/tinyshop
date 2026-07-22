from abc import ABC, abstractmethod

from tinyshop.domain.cart_Item import Cart
from tinyshop.domain.order import Order
from tinyshop.repositories.in_memory import CartInMemoryRepository, InMemoryOrderRepository
from tinyshop.repositories.protocols import CartRepository,OrderRepository
from tinyshop.application.storage import MemoryStorage
class AbstractUnitOfWork(ABC):
    carts: CartRepository
    orders:  OrderRepository

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()
    @abstractmethod
    def rollback(self): ...
    @abstractmethod
    def commit(self): ...

class InMemoryUnitOfWork(AbstractUnitOfWork):
    def __init__(self,in_memory_storage:MemoryStorage)-> None :
        self._session  = Session(in_memory_storage)
        self.carts =  CartInMemoryRepository(session=self._session)
        self.orders =  InMemoryOrderRepository(session=self._session)
        self._committed = False
        
    def rollback(self) -> None :
        self._session.clear()
        self._committed = False
    def commit(self)-> None :
        for order_id,order in self._session.new_orders.values():
            self._session.storage.add_order(order=order)
        for cart_id,cart  in self._session.new_carts.values():
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
    def add_cart(self, cart:Cart) -> None :
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




