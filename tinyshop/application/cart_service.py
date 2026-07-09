from typing import List

from tinyshop.domain.CartItem import Cart
from tinyshop.domain.Product import Product
from tinyshop.repositories.protocols import CartRepository


class CartService:
    def __init__(self,repo:CartRepository) -> None:
        self.repo = repo
    def create_cart(self,cart_id:int) -> Cart:
        cart =  Cart(id=cart_id)
        self.repo.add(cart)
        return cart
    def list_carts(self) -> List[Cart]:
        carts = self.repo.list()
        return list(carts)
    def remove_cart(self,cart_id:int) -> None:
        self.repo.remove(cart_id)
    def get_cart_by_id(self, cart_id:int) -> Cart:
        cart = self.repo.get(cart_id=cart_id)
        return cart
    def add_product_to_cart(self,product:Product,cart_id:int,quantity:int) -> Cart:
        cart = self.repo.get(cart_id=cart_id)
        cart.add_product(product=product,quantity=quantity)
        return cart
    def remove_product_from_cart(self,cart_id,product_id:int) ->Cart:
        cart = self.repo.get(cart_id=cart_id)
        cart.remove_product(product_id=product_id)
        return cart
    def change_product_quantity(self,cart_id:int,product_id:int,change:int) -> Cart:
        cart = self.repo.get(cart_id=cart_id)
        cart.change_quantity(product_id=product_id,change=change)
        return cart