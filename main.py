from abc import ABC, abstractmethod
from db import connect, close_connection,execute_query, create_inventory_table
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QDialog, QMessageBox
import sys

class Product(ABC):
    def __init__(self, product_id, product_name, product_price, product_qty):
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price
        self.product_qty = product_qty

    @abstractmethod
    def display(self):
        pass

class InventoryItem(Product):
    def __init__(self, product_id, product_name, product_price, product_qty):
        super().__init__(product_id, product_name, product_price, product_qty)

    def display(self):
        print(f"Product ID: {self.product_id}")
        print(f"Product Name: {self.product_name}")
        print(f"Product Price: Rp {self.product_price}")
        print(f"Product Quantity: {self.product_qty}")

class InventoryManager(ABC):
    @abstractmethod
    def add_product(self, product):
        pass

    @abstractmethod
    def remove_product(self, product_id):
        pass

    @abstractmethod
    def search_product(self, product_id):
        pass

    @abstractmethod
    def display_inventory(self):
        pass

class Inventory(InventoryManager):
    def add_product(self, product):
        con, cur = connect()
        try:
            query = "INSERT INTO inventory (product_id, product_name, product_price, product_qty) VALUES (%s, %s, %s, %s) ON CONFLICT (product_id) DO UPDATE SET product_name = %s, product_price = %s, product_qty = %s;"
            params = (product.product_id, product.product_name, product.product_price, product.product_qty, product.product_name, product.product_price, product.product_qty)
            cur.execute(query, params)
            con.commit()
            print("Product added to the inventory.")
        except Exception as error:
            print(f"Error adding product to database: {error}")
        finally:
            close_connection(con, cur)

    def remove_product(self, product_id):
        con, cur = connect()
        try:
            query = "DELETE FROM inventory WHERE product_id = %s;"
            params = (product_id,)
            cur.execute(query, params)
            con.commit()
            print("Product removed from the inventory.")
            return True
        except Exception as error:
            print(f"Error removing product from database: {error}")
            return False
        finally:
            close_connection(con, cur)

    def search_product(self, product_id):
        con, cur = connect()
        try:
            query = "SELECT * FROM inventory WHERE product_id = %s;"
            params = (product_id,)
            cur.execute(query, params)
            result = cur.fetchone()
            if result:
                print("\nProduct found.")
                product_id, product_name, product_price, product_qty = result
                return InventoryItem(product_id, product_name, product_price, product_qty)
            else:
                print("Product not found in the inventory.")
                return None
        except Exception as error:
            print(f"Error searching for product in database: {error}")
            return None
        finally:
            close_connection(con, cur)

    def display_inventory(self):
        con, cur = connect()
        try:
            query = "SELECT * FROM inventory;"
            cur.execute(query)
            rows = cur.fetchall()
            inventory = {}
            for row in rows:
                product_id, product_name, product_price, product_qty = row
                product = InventoryItem(product_id, product_name, product_price, product_qty)
                inventory[product_id] = product
            return inventory
        except Exception as error:
            print(f"Error displaying inventory from database: {error}")
            return {}
        finally:
            close_connection(con, cur)

class AddProductDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel('Add/Update Product:')
        layout.addWidget(self.label)

        self.product_id_label = QLabel('Product ID:')
        layout.addWidget(self.product_id_label)
        self.product_id_edit = QLineEdit()
        layout.addWidget(self.product_id_edit)

        self.product_name_label = QLabel('Product Name:')
        layout.addWidget(self.product_name_label)
        self.product_name_edit = QLineEdit()
        layout.addWidget(self.product_name_edit)

        self.product_price_label = QLabel('Product Price:')
        layout.addWidget(self.product_price_label)
        self.product_price_edit = QLineEdit()
        layout.addWidget(self.product_price_edit)

        self.product_qty_label = QLabel('Product Quantity:')
        layout.addWidget(self.product_qty_label)
        self.product_qty_edit = QLineEdit()
        layout.addWidget(self.product_qty_edit)

        self.add_button = QPushButton('Add/Update')
        self.add_button.clicked.connect(self.add_product)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_product(self):
        product_id = int(self.product_id_edit.text())
        product_name = self.product_name_edit.text()

        product_price_text = self.product_price_edit.text()
        product_qty_text = self.product_qty_edit.text()

        if product_price_text and product_qty_text:
            product_price = int(product_price_text)
            product_qty = int(product_qty_text)

            product = InventoryItem(product_id, product_name, product_price, product_qty)
            self.parent.inventory.add_product(product)

            QMessageBox.information(self, 'Success', 'Product added successfully.')

            self.accept()
        else:
            print("Please enter valid values for price and quantity")

class RemoveProductDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel('Remove Product:')
        layout.addWidget(self.label)

        self.product_id_label = QLabel('Product ID:')
        layout.addWidget(self.product_id_label)
        self.product_id_edit = QLineEdit()
        layout.addWidget(self.product_id_edit)

        self.remove_button = QPushButton('Remove')
        self.remove_button.clicked.connect(self.remove_product)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)

class RemoveProductDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel('Remove Product:')
        layout.addWidget(self.label)

        self.product_id_label = QLabel('Product ID:')
        layout.addWidget(self.product_id_label)
        self.product_id_edit = QLineEdit()
        layout.addWidget(self.product_id_edit)

        self.remove_button = QPushButton('Remove')
        self.remove_button.clicked.connect(self.remove_product)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)

    def remove_product(self):
        product_id = int(self.product_id_edit.text())
        if self.parent.inventory.remove_product(product_id):
            QMessageBox.information(self, 'Success', 'Product removed successfully.')
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Product not found in the inventory.')

class SearchProductDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel('Search Product:')
        layout.addWidget(self.label)

        self.product_id_label = QLabel('Product ID:')
        layout.addWidget(self.product_id_label)
        self.product_id_edit = QLineEdit()
        layout.addWidget(self.product_id_edit)

        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search_product)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def search_product(self):
        product_id = int(self.product_id_edit.text())
        result = self.parent.inventory.search_product(product_id)
        if result:
            product = result
            message = f"Product found!\n\nProduct ID: {product.product_id}\nProduct Name: {product.product_name}\nProduct Price: Rp {product.product_price}\nProduct Quantity: {product.product_qty}"
            QMessageBox.warning(self, 'Product Found', message)
        else:
            QMessageBox.warning(self, 'Product Not Found', 'Product not found in the inventory.')


class DisplayInventoryDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel('Display Inventory:')
        layout.addWidget(self.label)

        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)
        layout.addWidget(self.display_text)

        self.display_button = QPushButton('Display')
        self.display_button.clicked.connect(self.display_inventory)
        layout.addWidget(self.display_button)

        self.setLayout(layout)

    def display_inventory(self):
        self.display_text.clear()
        inventory_data = self.parent.inventory.display_inventory()
        if inventory_data:
            for product_id, product in inventory_data.items():
                self.display_text.append(f"\nProduct ID: {product_id}")
                self.display_text.append(f"Product Name: {product.product_name}")
                self.display_text.append(f"Product Price: Rp {product.product_price}")
                self.display_text.append(f"Product Quantity: {product.product_qty}")
        else:
            self.display_text.append("Inventory is empty.")
        self.show()

class ProductGUI(QWidget):
    def __init__(self, inventory):
        super().__init__()
        self.inventory = inventory
        self.add_product_dialog = None
        self.remove_product_dialog = None
        self.search_product_dialog = None
        self.display_inventory_dialog = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Inventory System')

        layout = QVBoxLayout()

        self.add_button = QPushButton('Add/Update Product')
        self.add_button.clicked.connect(self.show_add_dialog)
        layout.addWidget(self.add_button)

        self.remove_button = QPushButton('Remove Product')
        self.remove_button.clicked.connect(self.show_remove_dialog)
        layout.addWidget(self.remove_button)

        self.search_button = QPushButton('Search Product')
        self.search_button.clicked.connect(self.show_search_dialog)
        layout.addWidget(self.search_button)

        self.display_button = QPushButton('Display Inventory')
        self.display_button.clicked.connect(self.show_display_dialog)
        layout.addWidget(self.display_button)

        self.exit_button = QPushButton('Exit')
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def show_add_dialog(self):
        if not self.add_product_dialog or not self.add_product_dialog.isVisible():
            self.add_product_dialog = AddProductDialog(self)
            self.add_product_dialog.exec_()

    def show_remove_dialog(self):
        if not self.remove_product_dialog or not self.remove_product_dialog.isVisible():
            self.remove_product_dialog = RemoveProductDialog(self)
            self.remove_product_dialog.exec_()

    def show_search_dialog(self):
        if not self.search_product_dialog or not self.search_product_dialog.isVisible():
            self.search_product_dialog = SearchProductDialog(self)
            self.search_product_dialog.exec_()

    def show_display_dialog(self):
        if not self.display_inventory_dialog or not self.display_inventory_dialog.isVisible():
            self.display_inventory_dialog = DisplayInventoryDialog(self)
            self.display_inventory_dialog.exec_()

def main():
    create_inventory_table()
    inventory = Inventory()
    app = QApplication(sys.argv)
    gui = ProductGUI(inventory)
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()