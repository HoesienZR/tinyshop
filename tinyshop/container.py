from pathlib import Path

from tinyshop.repositories import JsonProductRepository,InMemoryProductRepository
from tinyshop.services import ProductService

def build_application():
    repo = InMemoryProductRepository()
    service = ProductService(repo)
    return service
