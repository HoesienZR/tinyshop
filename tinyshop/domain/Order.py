from dataclasses import dataclass, field
from typing import Tuple
from tinyshop.domain.models import Money, CartItem


@dataclass(frozen=True,slots=True)
class OrderItem:
    product_id: int = field()
    title: str = field()
    unit_price: Money = field()
    quantity: int = field(default=0)
    @property
    def total_price(self) -> Money:
        return self.unit_price * self.quantity
    def __post_init__(self):
        if  not isinstance(self.quantity,int) or isinstance(self.quantity, bool) or self.quantity <1 :
            raise ValueError("Quantity cannot be less than zero")
        title = self.title.strip()
        if not title:
            raise ValueError("Title cannot be empty")
        object.__setattr__(self,'title',title)
        if not isinstance(self.unit_price,Money) :
            raise ValueError("Unit price cannot be less than zero")
        if not isinstance(self.product_id,int) or isinstance(self.product_id, bool) or self.product_id <= 0  :
            raise ValueError("Product Id  cannot be less than zero")
    @classmethod
    def from_cart_item(cls, cart_item: CartItem) -> "OrderItem":
            return cls(product_id=cart_item.product_id,title=cart_item.title,quantity=cart_item.quantity,unit_price=cart_item.unit_price)
@dataclass(frozen=True,slots=True)
class Order:
    id : int  = field()
    items: Tuple[OrderItem] = field(default_factory=tuple)
    def __post_init__(self):
        if not isinstance(self.id,int) or isinstance(self.id, bool) or self.id <= 0 :
            raise ValueError("ID cannot be less than zero")
        if  not isinstance(self.items,tuple):
            raise ValueError("items are not tuple ")
        for item in self.items:
            if self.price_currency is not None  and  item.unit_price.currency != self.price_currency :
                raise ValueError("all the order item must be the same ")
    @property
    def price_currency(self) -> str|None:
        if self.items:
            return self.items[0].unit_price.currency
        return None
    @property
    def total_price(self)-> Money:
        if not self.items:
            raise ValueError("No items")
        return sum((item.total_price for item in self.items),start=Money(0,self.price_currency ))