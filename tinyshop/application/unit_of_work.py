from abc import ABC, abstractmethod

from tinyshop.repositories.in_memory import CartInMemoryRepository, InMemoryOrderRepository
from tinyshop.repositories.protocols import CartRepository,OrderRepository
from tinyshop.persistence import Session
from .storage import MemoryStorage
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
        for order_id,order in self._session.new_orders.items():
            self._session.storage.add_order(order=order)
        for cart_id,cart  in self._session.new_carts.items():
            self._session.storage.add_cart(cart=cart)
        self._session.clear()
        self._committed = True
    @property
    def session(self) -> "Session" :
        return self._session




