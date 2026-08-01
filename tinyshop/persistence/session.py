
from tinyshop.application.storage import MemoryStorage
from tinyshop.domain.cart_Item import  Cart
from tinyshop.domain.order import  Order


class Session:
    def __init__(self,storage:MemoryStorage) -> None:
        self.new_orders:dict[int, Order] = {}
        self.new_carts:dict[int , Cart] = {}
        self.deleted_orders:set[int] = set()
        self.deleted_carts:set[int] = set()
        self.storage = storage
    def add_order(self, order: Order) -> None :
        if order.id in self.deleted_orders:
            self.deleted_orders.discard(order.id)
        self.new_orders.update({order.id:order})
    def add_cart(self, cart:Cart) -> None :
        if cart.id in self.deleted_carts:
            self.deleted_carts.discard(cart.id)
        self.new_carts.update({cart.id:cart})
    def clear(self)-> None :
        self.new_orders.clear()
        self.new_carts.clear()
        self.deleted_orders.clear()
        self.deleted_carts.clear()
    def get_order(self, order_id:int) -> Order:
        if order_id in self.deleted_orders:
            raise ValueError("Order id {} was deleted".format(order_id))
        order = self.new_orders.get(order_id, None)
        if order is None:
            order = self.storage.get_order(order_id)
            if order is None:
                raise ValueError(f"Order {order_id} not found")
        return order
    def get_cart(self, cart_id:int) -> Cart:
        if cart_id in self.deleted_carts:
            raise ValueError("Cart id {} was deleted".format(cart_id))
        cart = self.new_carts.get(cart_id, None)
        if cart is None:
            cart = self.storage.get_cart(cart_id)
            if cart is None:
                raise ValueError(f"Cart {cart_id} not found")
        return cart
    def remove_cart(self, cart_id:int) -> None :
        result = self.new_carts.pop(cart_id, None)
        if result is None :
            result = self.storage.get_cart(cart_id)
            if result is None :
                raise ValueError(f"Cart {cart_id} not found")
            self.deleted_carts.add(cart_id)

    def remove_order(self, order_id:int) -> None :
        result = self.new_orders.pop(order_id, None)
        if result is None :
            result = self.storage.get_order(order_id)
            if result is None :
                raise ValueError("order didn't found ")
            self.deleted_orders.add(order_id)
    def cart_list(self) -> list[Cart]:
        storage_cart_ids = self.storage.list_cart_ids()
        new_cart_ids = self.new_carts.keys()
        all_carts = set(storage_cart_ids).union(new_cart_ids).difference(set(self.deleted_carts))
        carts = []
        for cart_id in all_carts:
            carts.append(self.get_cart(cart_id))
        return carts
    def order_list(self)-> list[Order] :
        storage_orders_ids = self.storage.list_order_ids()
        new_order_ids = self.new_orders.keys()
        all_orders = set(storage_orders_ids).union(new_order_ids).difference(set(self.deleted_orders))
        orders = []
        for order_id in all_orders:
            orders.append(self.get_order(order_id))
        return orders


