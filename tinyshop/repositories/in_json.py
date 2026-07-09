import json
from pathlib import Path
from typing import Iterable

from tinyshop.domain.product import Product
from tinyshop.repositories.protocols import ProductRepository


class JsonProductRepository(ProductRepository):
    def __init__(self ,path :Path) -> None:
        self._file = Path(path)
        self._products = self._load()


    def _load(self) -> dict[int, Product]:
        if not self._file.exists():
            return {}
        try :
            with open(self._file ,'r') as f:
                data = json.load(f)
            return {
                int(pid) :Product.from_dict(product) for pid, product in data.items()
            }
        except (json.JSONDecodeError, ValueError):
            return {}
    def _save(self )-> None:
        with open(self._file ,'w') as f:
            json.dump({
                pid :product.to_dict()
                for pid ,product in self._products.items()
            },
                f,
                indent=4)
    def add(self ,product: Product) -> None:
        if   product.id   in self._products:
            raise ValueError(f'Product {product.id} already exists')
        self._products[product.id] = product
        self._save()
    def get(self, product_id :int) -> Product:
        try:
            return self._products[product_id]
        except KeyError:
            raise ValueError("Product not found")
    def remove(self, product_id :int) -> None:
        if product_id not in self._products:
            raise ValueError("Product not found")
        del self._products[product_id]
        self._save()
    def list(self )->Iterable[Product]:
        return self._products.values()

