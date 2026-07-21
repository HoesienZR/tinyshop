from tinyshop.domain.cart_Item import Cart
from tinyshop.domain.order import Order


class MemoryStorage:
    orders: dict[int, Order] = {}
    carts: dict[int, Cart] = {}
    def add_order(self, order:Order) -> None :
        self.orders[order.id] = order
    def add_cart(self, cart:Cart) -> None :
        self.carts[cart.id] = cart
    def get_cart(self, cart_id:int) -> Cart :
        return self.carts.get(cart_id, None)
    def get_order(self, order_id:int) -> Order:
        return self.orders.get(order_id, None)