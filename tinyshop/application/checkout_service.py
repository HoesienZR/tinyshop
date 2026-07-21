from tinyshop.domain.order import Order, OrderItem
from tinyshop.application.unit_of_work import InMemoryUnitOfWork,AbstractUnitOfWork

class CheckoutService:
    def __init__(self,
                 uow : AbstractUnitOfWork) -> None:
        self.uow = uow
    def checkout(self,cart_id:int,order_id:int ) -> Order:
        with self.uow:
            cart = self.uow.carts.get(cart_id=cart_id)
            if not cart.items:
                #TODO cart not found error
                raise ValueError(f"No items in  found in cart with item {cart_id}")
            order_items = [ OrderItem.from_cart_item(item ) for item in cart.items ]
            order = Order(id=order_id,items= tuple(order_items))
            self.uow._session.add_new_order(order=order)
            self.uow._session.add_delete_carts(cart_id=cart_id)
            self.uow.commit()
        return order

