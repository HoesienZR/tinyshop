import pytest

from tinyshop.domain.models import Product, Money

def test_create_product():
    m1 = Money(amount=12, currency="IRR")
    p1 = Product(title="test",id=1,price=m1)
    assert p1.title == "test"
    assert p1.id == 1
    assert p1.price == m1
def test_create_product_with_empty_title():
    m1 = Money(amount=12, currency="IRR")
    with pytest.raises(ValueError):
        Product(title="",id=1,price=m1)


def test_create_product_with_empty_price():
    with pytest.raises(TypeError):
        Product(title="test",id=1,)



def test_apply_discount_product():
    m1 = Money(amount=100, currency="IRR")
    p1 = Product(title="test",id=1,price=m1)
    discounted_product = p1.apply_discount(10)
    print(discounted_product)
    assert discounted_product.title == "test"
    assert discounted_product.id == 1
    assert discounted_product.price.amount == 90

def test_apply_discount_product_with_under_zero_percent():
    m1 = Money(amount=100, currency="IRR")
    p1 = Product(title="test",id=1,price=m1)
    with pytest.raises(ValueError):
         p1.apply_discount(-1)
def test_apply_discount_product_with_over_zero_percent():
    m1 = Money(amount=100, currency="IRR")
    p = Product(title="test",id=1,price=m1)
    with pytest.raises(ValueError):
        p.apply_discount(101)

def test_create_product_with_none_title():
    m1 = Money(amount=12, currency="IRR")
    with pytest.raises(ValueError):
        p1 = Product(id=1,price=m1)
def test_create_product_with_empty_id():
    m1 = Money(amount=12, currency="IRR")
    p1 = Product(title="test",price=m1)
    assert p1.title == "test"
    assert p1.price == m1

def test_product_equality():
    m1 = Money(amount=12, currency="IRR")
    m2 = Money(amount=12, currency="IRR")
    p1 = Product(price=m1,title="test",id=1)
    p2 = Product(price=m1,title="test",id=2)
    assert p1 != p2
def test_apply_discount_return_new_product_with_discounted_price():
    product = Product(price=Money(amount=100, currency="IRR"), title="test", id=1)
    discounted_product = product.apply_discount(80)
    assert discounted_product.title == product.title
    assert discounted_product.id == product.id
    assert discounted_product.price.amount == 20

def test_discounted_product_does_not_mutate_orginal_price():
    product = Product(price=Money(amount=100, currency="IRR"), title="test", id=1)
    discounted_product = product.apply_discount(80)
    assert product.price.amount == 100
    assert discounted_product.price.amount == 20
    assert discounted_product is not product
def test_apply_zero_discount_keeps_same_amount():
    product = Product( price=Money(amount=100, currency="USD"),title="Clean Code",id=1,)
    discounted = product.apply_discount(0)
    assert discounted.price.amount == 100

def test_apply_discount_rejects_bool_percent():
    product = Product(
        price=Money(amount=100, currency="USD"),
        title="Clean Code",
        id=1,
    )

    with pytest.raises(ValueError):
        product.apply_discount(True)