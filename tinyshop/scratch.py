# scratch.py

from tinyshop.domain.models import Money, Product

cases = [
    lambda: Money(100, "USD"),
    lambda: Money(0, "USD"),
    lambda: Money(-1, "USD"),
    lambda: Money(100, "usd"),
    lambda: Money(100, "USDD"),
    lambda: Money(100, "U1D"),
    lambda: Product(Money(100, "USD"), "Book", 1),
    lambda: Product(Money(100, "USD"), "", 1),
    lambda: Product(Money(100, "USD"), "   ", 1),
    lambda: Product(Money(100, "USD"), "Book", 0),
]

for case in cases:
    try:
        print(case())
    except Exception as e:
        print(type(e).__name__, e)
