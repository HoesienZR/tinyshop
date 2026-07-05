import pytest

from tinyshop.domain.models import Product
from tinyshop.services import ProductService,CartService
from tinyshop.repositories import InMemoryProductRepository,CartInMemoryRepository


@pytest.fixture
def service():
    repo = InMemoryProductRepository()
    return ProductService(repo=repo)
@pytest.fixture
def cart_service():
    repo = CartInMemoryRepository()
    return CartService(repo=repo)
def test_create_product_by_service(service: ProductService):

    product = service.create_product(product_id=1,title="test",currency="IRR",amount=100)
    assert product.title == "test"
    assert product.price.amount == 100
    assert product.id == 1
    assert product.price.currency == "IRR"
def test_two_create_products_with_the_same_id_by_service(service: ProductService):
    service.create_product(product_id=1, title="test", currency="IRR", amount=100)
    with pytest.raises(ValueError):
        service.create_product(product_id=1, title="test", currency="IRR", amount=100)
def test_create_product_then_apply_discount_by_service(service: ProductService):
    product = service.create_product(product_id=1,title="test",currency="IRR",amount=100)
    discounted_product = service.apply_discount(percent=10,product_id=product.id)
    assert discounted_product.id == product.id
    assert discounted_product != product
    assert discounted_product.price.amount == 90
def  test_remove_product_then_get_raises_error(service: ProductService):
    product = service.create_product(product_id=1, title="test", currency="IRR", amount=100)
    service.remove_product(product_id=product.id)
    with pytest.raises(ValueError):
        service.get_product_by_id(product_id=product.id)

#def test_search_returns_products_matching_query(service: ProductService):
#    products = service.search_products("phone")
#    assert len(products) > 0
#    for product in products:
#        assert  "phone" in product.title.lower()

def test_get_all_product_with_in_sensitive_query(service: ProductService):
    query = "Apple"
    products = service.search_products(query)
    for product in products:
        assert "Apple".lower() in product.title.lower()
def test_all_product_with_empty_query(service: ProductService):
    searched_products = service.search_products("")
    all_products = service.list_products()
    assert searched_products == all_products
    assert len(searched_products) == len(all_products)
def test_search_query_with_spaces_query(service: ProductService):
    searched_products = service.search_products("          ")
    all_products = service.list_products()
    assert searched_products == all_products
    assert len(searched_products) == len(all_products)
def test_search_product_with_no_existent_product(service: ProductService):
    searched_products = service.search_products("aisdfhiuoashfioq auifhu9asdf asdf")
    assert len(searched_products) == 0
def test_search_product_with_long_query(service: ProductService):
    query = "Apple IPhone"
    searched_products = service.search_products(query)
    for product in searched_products:
        assert query.lower() in product.title.lower()
def test_search_query_with_trim_query(service: ProductService):
    query = "      Apple          "
    searched_products = service.search_products(query)
    for product in searched_products:
        assert query.strip().lower() in product.title.lower()
def test_create_cart_with_service(cart_service: CartService):
    cart = cart_service.create_cart(cart_id=2)
    assert cart_service.get_cart_by_id(2) is cart
def test_get_cart_with_service(cart_service: CartService):
    cart = cart_service.create_cart(cart_id=1)
    assert cart_service.get_cart_by_id(1).id == cart.id
    assert cart_service.get_cart_by_id(1) is  cart
def test_remove_cart_with_service(cart_service: CartService):
    cart = cart_service.create_cart(cart_id=2)
    cart_service.remove_cart(cart_id=2)
    with pytest.raises(ValueError):
        cart_service.get_cart_by_id(cart_id=2)
def test_list_carts_with_service(cart_service: CartService):
    cart = cart_service.create_cart(cart_id=1)
    cart2 = cart_service.create_cart(cart_id=2)
    assert len(cart_service.list_carts()) == 2
def test_add_product_to_cart_with_service(cart_service: CartService,service: ProductService):
    cart = cart_service.create_cart(cart_id=1)
    product = service.create_product(product_id=1,title="test",currency="IRR",amount=100)
    cart_service.add_product_to_cart(product=product,quantity=10,cart_id=cart.id)
    assert len(cart.items) == 1
    assert cart.items[0].quantity == 10
    assert cart.items[0].product_id == 1
def test_remove_product_from_cart_with_service(cart_service: CartService,service: ProductService):
    cart = cart_service.create_cart(cart_id=1)
    product = service.create_product(product_id=1,title="test",currency="IRR",amount=100)
    cart.add_product(product,quantity=2)
    cart_service.remove_product_from_cart(cart_id=1,product_id=1)
    assert len(cart.items) == 0
def test_change_product_quantity(cart_service: CartService,service: ProductService):
    cart = cart_service.create_cart(cart_id=1)
    product = service.create_product(product_id=1, title="test", currency="IRR", amount=100)
    cart.add_product(product, quantity=2)
    cart.change_quantity(product_id=1,change=3)
    assert cart.items[0].quantity == 5