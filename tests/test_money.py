from tinyshop.errors import CurrencyMismatchError
from tinyshop.domain.models import Money
import pytest

def test_create_money():
    money  = Money(amount=100, currency='USD')
    assert money.amount == 100
    assert money.currency == 'USD'
def test_create_money_with_negetive_amount():
    with pytest.raises(ValueError):
        Money(amount=-1, currency='USD')
def test_add_money() -> None:
    m1 = Money(amount=12,currency="IRR")
    m2 = Money(amount=8,currency="IRR")

    result = m1 + m2
    assert result.amount == 20
    assert result.currency == "IRR"

def test_subtract_money_on_failure() -> None:
    m1 = Money(amount=12, currency="IRR")
    m2 = Money(amount=8, currency="IRR")
    with pytest.raises(ValueError):
        m2 - m1
def test_subtract_money_on_success() -> None:
    m1 = Money(amount=12, currency="IRR")
    m2 = Money(amount=8, currency="IRR")
    result = m1 - m2
    assert result.amount == 4
    assert result.currency == "IRR"

def test_unmatch_currency()->None:
    m1 = Money(amount=12, currency="IRR")
    m2 = Money(amount=8, currency="USD")
    with pytest.raises(CurrencyMismatchError):
        m1 + m2


def test_normalize_currency() -> None:
    m1 = Money(amount=12, currency="  irr   ")
    assert m1.currency == "IRR"


def test_same_money_is_equal() -> None:
    m1 = Money(amount=12, currency="IRR")
    m2 = Money(amount=12, currency="IRR")

    assert m1 == m2
    assert m1 is not m2
def test_money_is_immutable() -> None:
    m1 = Money(amount=12, currency="IRR")
    with pytest.raises(AttributeError):
        m1.amount = 12
def test_create_product_with_empty_amount():
    m1 = Money( currency="IRR")