
from tinyshop.errors import CurrencyMismatchError
from tinyshop.domain.models import Cart, CartItem, Product, Money
import pytest

from tinyshop.repositories import InMemoryProductRepository
from tinyshop.services import ProductService


@pytest.fixture
def service():
    repo = InMemoryProductRepository()
    return ProductService(repo=repo)
def test_add_same_to_products_to_cart(service: ProductService):
    p1 = service.create_product(product_id=1,title="Iphone",currency="IRR",amount=100)
    cart = Cart(id=1)
    cart.add_product(p1,2)
    cart.add_product(p1,3)
    assert len(cart.items) == 1
    assert cart.items[0].quantity == 5
def test_add_two_different_product_in_cart(service):
    p1 = service.create_product(product_id=1,title="Iphone",currency="IRR",amount=100)
    p2 = service.create_product(product_id=2,title="SamSong",currency="IRR",amount=100)
    cart = Cart(id=1)
    cart.add_product(p1,2)
    cart.add_product(p2,3)
    assert len(cart.items) == 2
def test_remove_product_from_cart(service):
    p1 = service.create_product(product_id=1, title="Iphone", currency="IRR", amount=100)
    cart = Cart(id=1)
    cart.add_product(p1,quantity=2)
    cart.remove_product(product_id=1)
    assert len(cart.items) == 0
def test_total_price_in_cart(service):
    p1 = service.create_product(product_id=1,title="Iphone",currency="IRR",amount=100)
    p2 = service.create_product(product_id=2,title="SamSong",currency="IRR",amount=100)
    cart = Cart(id=1)
    cart.add_product(p1, quantity=2)
    cart.add_product(p2, quantity=2)
    price:Money = cart.total_price()
    assert isinstance(price, Money)
    assert price.amount == 400
    assert price.currency == "IRR"

def test_cart_change_quantity(service):
    p1=service.create_product(product_id=1,title="Iphone",currency="IRR",amount=100)
    cart=Cart(id=1)
    cart.add_product(p1,quantity=2)
    cart.change_quantity(product_id=1,change=2)
    print(cart.items)
    assert cart.items[0].quantity == 4
def test_change_product_quantity_less_than_zero(service):
    p1 = service.create_product(product_id=1, title="Iphone", currency="IRR", amount=100)
    cart = Cart(id=1)
    cart.add_product(p1,quantity=2)
    cart.change_quantity(product_id=1,change=-2)

    assert len(cart.items) == 0
def tset_add_two_product_with_different_currency_in_cart(service):
    p1 = service.create_product(product_id=1, title="Iphone", currency="IRR", amount=100)
    p2 = service.create_product(product_id=1, title="Iphone", currency="USD", amount=100)
    cart = Cart(id=1)
    cart.add_product(p1,quantity=2)
    with pytest.raises(CurrencyMismatchError):
        cart.add_product(p2,quantity=2)

