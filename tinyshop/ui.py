from tinyshop.services import ProductService


def run_cli(service: ProductService) -> None:
    while True:
        print("\n=== TinyShop CLI ===")
        print("1. Add product")
        print("2. Get product")
        print("3. List products")
        print("4. Remove product")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            _add_product(service)
        elif choice == "2":
            _get_product(service)
        elif choice == "3":
            _list_products(service)
        elif choice == "4":
            _remove_product(service)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

def _add_product(service: ProductService) -> None:
    try :
        product_id = int(input("Enter product id: "))
        currency = input("Enter currency: ")
        title = input("Enter title: ")
        amount = int(input("Enter amount: "))
        product = service.create_product(product_id=product_id,title=title, amount=amount,currency= currency)
        print(f"product added {product}")
    except Exception as e :
        print(f"Error {e}")
def _get_product(service: ProductService) -> None:
    try:
        product_id = int(input("Enter product id: "))
        product = service.get_product_by_id(product_id=product_id)
        print(f"product:{product} returned")
    except Exception as e :
        print(f"Error {e}")
def _list_products(service: ProductService) -> None:
    try :
        products = service.list_products()
        for product in products:
            print(product)
    except Exception as e :
        print(f"Error {e}")
def _remove_product(service: ProductService) -> None:
    try :
        product_id = int(input("Enter product id: "))
        service.remove_product(product_id=product_id)
        print(f"removed product {product_id}")
    except Exception as e :
        print(f"Error {e}")
