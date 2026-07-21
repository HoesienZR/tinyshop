from tinyshop.container import build_application
from ui import run_cli







if __name__ == '__main__':
    service = build_application()
    print("Application started")
    run_cli(service)

