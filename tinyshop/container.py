from pathlib import Path

from tinyshop.repositories import JsonProductRepository,InMemoryProductRepository
from tinyshop.application import ProductService

def build_application():
    repo = InMemoryProductRepository()
    service = ProductService(repo)
    return service
