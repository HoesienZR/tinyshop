import pytest


from tinyshop.application.unit_of_work import InMemoryUnitOfWork
from tinyshop.persistence.session import  Session
from tinyshop.application.storage import MemoryStorage
from tinyshop.repositories.in_memory import InMemoryOrderRepository, CartInMemoryRepository

from tinyshop.domain.cart_Item import CartItem,Cart
from tinyshop.domain.order import OrderItem,Order
from tinyshop.domain.money import Money
from tinyshop.domain.product import Product
@pytest.fixture
def memory_storage():
    return MemoryStorage()
@pytest.fixture
def session(memory_storage):
    return Session(memory_storage)

@pytest.fixture
def unit_of_work_fixture(memory_storage):
    uow = InMemoryUnitOfWork(memory_storage)
    return uow
def test_unit_of_work(unit_of_work_fixture):
    order = Order(id=1)
    cart = Cart(id=1)
    unit_of_work_fixture.session.add_cart(cart)
    unit_of_work_fixture.session.add_order(order)
    unit_of_work_fixture.commit()
    assert unit_of_work_fixture.session.storage.get_cart(cart.id).id == 1
    assert unit_of_work_fixture.session.storage.get_order(order.id).id == 1
    assert unit_of_work_fixture.session.get_order(order.id).id == 1 and isinstance(unit_of_work_fixture.session.get_order(order.id), Order)
    assert unit_of_work_fixture.session.storage.get_cart(cart.id).id == 1  and isinstance(unit_of_work_fixture.session.storage.get_cart(cart.id),Cart)
