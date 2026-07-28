import pytest

from tinyshop.application.storage import MemoryStorage
from tinyshop.application.unit_of_work import InMemoryUnitOfWork, Session
from tinyshop.repositories.in_memory import InMemoryOrderRepository, CartInMemoryRepository
from tinyshop.application.storage import MemoryStorage
from tinyshop.domain import Product,Money,OrderItem,Order,CartItem,Cart
@pytest.fixture
def unit_of_work_fixture():
    storage  = MemoryStorage()
    uow = InMemoryUnitOfWork(storage)
    return uow
def test_unit_of_work(unit_of_work_fixture):
    order = Order(id=1)
    cart = Cart(id=1)
    unit_of_work_fixture.session.add_cart(cart)
    unit_of_work_fixture.session.add_new_order(order)
    unit_of_work_fixture.commit()
    assert unit_of_work_fixture.session.storage.get_cart(cart.id) == 1
    assert unit_of_work_fixture.session.storage.get_order(order.id) == 1
    with pytest.raises(ValueError):
         unit_of_work_fixture.session.get_order(order.id)
    with pytest.raises(ValueError):
        unit_of_work_fixture.session.get_cart(cart.id)