from db import create_inventory_table
from inventory import Inventory
from PyQt5.QtWidgets import QApplication
from ui import ProductGUI
import sys


def main():
    create_inventory_table()
    inventory = Inventory()
    app = QApplication(sys.argv)
    gui = ProductGUI(inventory)
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()