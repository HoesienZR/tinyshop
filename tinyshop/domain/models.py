from dataclasses import dataclass, field ,replace
from typing import List



from tinyshop.errors import CurrencyMismatchError
@dataclass(frozen=True,slots=True)
class Money:
    amount:int = field(default=0)
    currency:str = field(default='USD')
    def __sub__(self, other:"Money")->"Money":
        if  not  isinstance(other , Money) :
            return NotImplemented
        if  self.currency != other.currency:
            raise CurrencyMismatchError("Currencies must match")
        total_amount = self.amount - other.amount
        if total_amount < 0:
            raise ValueError('Amounts must not be negative')
        return Money(amount=total_amount, currency=self.currency)
    def __add__(self, other:"Money")->"Money":
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise CurrencyMismatchError("Currencies must match")
        total_amount = self.amount + other.amount
        return Money(amount=total_amount, currency=self.currency)
    def __mul__(self, other: int)->"Money":
        if isinstance(other, int) and not  isinstance(other, bool):
            if other < 0 :
                raise ValueError('Amounts must not be negative')
            multiplied_money = Money(amount=self.amount*other, currency=self.currency)
            return multiplied_money
        else :
            return NotImplemented
    def __rmul__(self, other)->"Money":
        return self.__mul__(other)
    def __post_init__(self,):

        if not isinstance(self.currency, str):
            raise ValueError("Enter a valid string for currency ")
        currency_sign = self.currency.strip().upper()
        if not (len(currency_sign) == 3 and   currency_sign.isalpha()):
            raise ValueError("enter a valid currency code")

        if   not isinstance(self.amount, int) or  isinstance(self.amount, bool)  :
            raise ValueError("enter a integer  number")
        if not self.amount >= 0 :
            raise ValueError('amount cannot be negative')
        object.__setattr__(self,'currency', currency_sign)

    def to_dict(self) -> dict:
        return {"amount":self.amount,
                "currency":self.currency}
    @classmethod
    def from_dict(cls,data:dict) -> "Money":
        return cls(amount=data['amount'],currency=data['currency'])
    def __repr__(self):
        return f"Money(amount={self.amount}, currency={self.currency!r})"




@dataclass(slots=True,frozen=True)
class Product:
    price: Money
    id:int = field(default=0)
    title:str = field(default='')

    def __post_init__(self,):
        if not isinstance(self.title, str):
            raise ValueError("Enter a valid string for title")
        title = self.title.strip()
        if len(title) == 0 :
            raise ValueError("Enter a valid string for title")
        if not (isinstance(self.id, int) and self.id >= 0) :
            raise ValueError("Enter a valid integer for id")
        if not isinstance(self.price,Money):
            raise ValueError("Price is not a Money Object ")

        object.__setattr__(self,'title', title)

    def __repr__(self):
        return f"Product(price={self.price}, id={self.id}, title={self.title!r})"
    def to_dict(self) -> dict:
        return {"id":self.id,"title":self.title,"price":self.price.to_dict()}
    @classmethod
    def from_dict(cls, data: dict) ->"Product":
        money = data['price']

        product_id = data['id']
        title = data['title']
        product = cls(price=Money.from_dict(money), id=product_id, title=title)
        return product
    def apply_discount(self,offer:int) -> "Product":
        if not isinstance(offer, int) or  isinstance(offer, bool) :
            raise ValueError("Enter a valid integer for offer")
        if offer < 0 :
            raise ValueError('Offer cannot be negative')
        if offer > 100 :
            raise ValueError('Offer cannot be greater than 100')
        amount = self.price.amount
        currency = self.price.currency
        new_amount = amount * (100 - offer)//100
        new_price = Money(amount=new_amount, currency=currency)
        return replace(self,price=new_price)


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


