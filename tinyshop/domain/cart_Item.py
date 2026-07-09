from dataclasses import dataclass, field
from typing import List

from tinyshop.domain.Money import Money
from tinyshop.domain.Product import Product
from tinyshop.errors import CurrencyMismatchError


@dataclass(slots=True,)
class CartItem:
    product_id:int
    title:str
    unit_price:Money
    quantity:int
    def __post_init__(self):
        if not isinstance(self.quantity, int)  or  self.quantity <= 0 or  isinstance(self.quantity, bool) :
            raise ValueError("Quantity cannot be less than zero" )
        if not isinstance(self.unit_price,Money) :
            raise ValueError("UnitPrice is not a Money Object ")
        title = self.title.strip()
        if   len(title) ==0 :
            raise ValueError("Enter a valid string for title")
        setattr(self,'title', title)
        if not (isinstance(self.product_id, int) and self.product_id >= 0):
            raise ValueError("Enter a valid integer for id")


@dataclass(slots=True)
class Cart:
    id:int
    items: List[CartItem] = field(default_factory=list)

    @property
    def cart_currency(self):
        if  self.items:
            return self.items[0].unit_price.currency
        return None
    def add_product(self,product:Product,quantity:int) -> None:
        if not isinstance(product,Product) :
            raise ValueError(" is not a Product")
        if not  isinstance(quantity, int) or  isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Quantity cannot be greater  zero")
        if self.items and product.price.currency != self.cart_currency :
            raise CurrencyMismatchError("Currencies must match")
        for item in self.items:
            if product.id == item.product_id:
                self.change_quantity(change=quantity,product_id=item.product_id)
                return None
        new_item = CartItem(product_id=product.id,title=product.title,unit_price=product.price,quantity=quantity)
        self.items.append(new_item)


    def remove_product(self,product_id:int) -> bool:
        for item in self.items:
            if item.product_id == product_id:
                self.items.remove(item)
                return True
        return False

    def total_price(self)->Money:
        if not self.items:
            return Money(currency="USD")
        currency  = self.items[0].unit_price.currency
        total = Money(amount=0, currency=currency)
        for item in self.items:
            sub_total_price = item.unit_price * item.quantity
            total += sub_total_price
        return total
    def change_quantity(self, product_id, change: int) -> None:
        if not isinstance(product_id, int) or  isinstance(product_id, bool) :
            raise ValueError("Enter a valid integer for product_id")
        if not isinstance(change, int) or  isinstance(change, bool)   :
            raise ValueError("Enter a valid integer for change")
        for item in self.items:
            if item.product_id == product_id:
                new_quantity = item.quantity + change
                if new_quantity  <= 0 :
                    self.items.remove(item)
                    break
                item.quantity = new_quantity
                break

