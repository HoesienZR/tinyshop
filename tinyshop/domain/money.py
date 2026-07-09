from dataclasses import dataclass, field

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