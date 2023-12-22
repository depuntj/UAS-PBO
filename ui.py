from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)

from inventory import InventoryItem


class AddProductDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Add/Update Product:")
        layout.addWidget(self.label)

        self.product_id_label = QLabel("Product ID:")
        layout.addWidget(self.product_id_label)
        self.product_id_edit = QLineEdit()
        layout.addWidget(self.product_id_edit)

        self.product_name_label = QLabel("Product Name:")
        layout.addWidget(self.product_name_label)
        self.product_name_edit = QLineEdit()
        layout.addWidget(self.product_name_edit)

        self.product_price_label = QLabel("Product Price:")
        layout.addWidget(self.product_price_label)
        self.product_price_edit = QLineEdit()
        layout.addWidget(self.product_price_edit)

        self.product_qty_label = QLabel("Product Quantity:")
        layout.addWidget(self.product_qty_label)
        self.product_qty_edit = QLineEdit()
        layout.addWidget(self.product_qty_edit)

        self.add_button = QPushButton("Add/Update")
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

            product = InventoryItem(
                product_id, product_name, product_price, product_qty
            )
            self.parent.inventory.add_product(product)

            QMessageBox.information(self, "Success", "Product added successfully.")

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

        self.label = QLabel("Remove Product:")
        layout.addWidget(self.label)

        self.product_id_label = QLabel("Product ID:")
        layout.addWidget(self.product_id_label)
        self.product_id_edit = QLineEdit()
        layout.addWidget(self.product_id_edit)

        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_product)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)

    def remove_product(self):
        product_id = int(self.product_id_edit.text())
        if self.parent.inventory.remove_product(product_id):
            QMessageBox.information(self, "Success", "Product removed successfully.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Product not found in the inventory.")


class SearchProductDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Search Product:")
        layout.addWidget(self.label)

        self.product_id_label = QLabel("Product ID:")
        layout.addWidget(self.product_id_label)
        self.product_id_edit = QLineEdit()
        layout.addWidget(self.product_id_edit)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_product)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def search_product(self):
        product_id = int(self.product_id_edit.text())
        result = self.parent.inventory.search_product(product_id)
        if result:
            product = result
            message = f"Product found!\n\nProduct ID: {product.product_id}\nProduct Name: {product.product_name}\nProduct Price: Rp {product.product_price}\nProduct Quantity: {product.product_qty}"
            QMessageBox.warning(self, "Product Found", message)
        else:
            QMessageBox.warning(
                self, "Product Not Found", "Product not found in the inventory."
            )


class DisplayInventoryDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Display Inventory:")
        layout.addWidget(self.label)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        self.display_button = QPushButton("Display")
        self.display_button.clicked.connect(self.display_inventory)
        layout.addWidget(self.display_button)

        self.setLayout(layout)

    def display_inventory(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

        header_labels = [
            "Product ID",
            "Product Name",
            "Product Price",
            "Product Quantity",
        ]
        self.table_widget.setColumnCount(len(header_labels))
        self.table_widget.setHorizontalHeaderLabels(header_labels)

        inventory_data = self.parent.inventory.display_inventory()
        if inventory_data:
            for product_id, product in inventory_data.items():
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)

                self.table_widget.setItem(
                    row_position, 0, QTableWidgetItem(str(product_id))
                )
                self.table_widget.setItem(
                    row_position, 1, QTableWidgetItem(product.product_name)
                )
                self.table_widget.setItem(
                    row_position, 2, QTableWidgetItem(f"Rp {product.product_price}")
                )
                self.table_widget.setItem(
                    row_position, 3, QTableWidgetItem(str(product.product_qty))
                )
        else:
            self.table_widget.setRowCount(1)
            self.table_widget.setItem(0, 0, QTableWidgetItem("Inventory is empty."))

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
        self.setWindowTitle("Inventory System")

        layout = QVBoxLayout()

        self.add_button = QPushButton("Add/Update Product")
        self.add_button.clicked.connect(self.show_add_dialog)
        layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Product")
        self.remove_button.clicked.connect(self.show_remove_dialog)
        layout.addWidget(self.remove_button)

        self.search_button = QPushButton("Search Product")
        self.search_button.clicked.connect(self.show_search_dialog)
        layout.addWidget(self.search_button)

        self.display_button = QPushButton("Display Inventory")
        self.display_button.clicked.connect(self.show_display_dialog)
        layout.addWidget(self.display_button)

        self.exit_button = QPushButton("Exit")
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
        if (
            not self.display_inventory_dialog
            or not self.display_inventory_dialog.isVisible()
        ):
            self.display_inventory_dialog = DisplayInventoryDialog(self)
            self.display_inventory_dialog.exec_()
