import typer

from tinyshop.__main__ import build_application
app = typer.Typer()

services = build_application()

@app.command()
def create(id:int,title:str, amount:int,currency:str="USD")->None:
    product =  services.createProduct(id=id, title=title, price=amount, currency=currency)

    print(f"created Product:{product.title} with price:{product.price}")




@app.command()
def list_products()->None:
    products = services.listProducts()
    for product in products:
        print(f"created Product:{product.title} with price:{product.price}")


@app.command()
def apply_discount(id:int,percent:int)->None:
    product = services.apply_discount(id=id,percent=percent)
    print(f"applied Product:{product.title} with price:{product.price}")

if __name__ == "__main__":
    app()