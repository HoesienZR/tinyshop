from dataclasses import dataclass, field, replace

from tinyshop.domain.Money import Money


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
