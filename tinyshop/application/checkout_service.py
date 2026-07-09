from tinyshop.domain.Order import Order, OrderItem
from tinyshop.repositories.protocols import CartRepository, OrderRepository


class CheckoutService:
    def __init__(self,
                 cart_repository:CartRepository,
                 order_repository:OrderRepository) -> None:
        self.cart_repository = cart_repository
        self.order_repository = order_repository
    def checkout(self,cart_id:int,order_id:int ) -> Order:
        cart = self.cart_repository.get(cart_id=cart_id)
        if not cart.items:
            raise ValueError(f"No items in  found in cart with item {cart_id}")
        order_items = [ OrderItem.from_cart_item(item ) for item in cart.items ]
        order = Order(id=order_id,items= tuple(order_items))
        self.order_repository.add(order=order)
        self.cart_repository.remove(cart_id=cart_id)
        return order

