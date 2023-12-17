from abc import ABC, abstractmethod
from db import (
    connect,
    close_connection,
    execute_query,
)


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
            params = (
                product.product_id,
                product.product_name,
                product.product_price,
                product.product_qty,
                product.product_name,
                product.product_price,
                product.product_qty,
            )
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
                return InventoryItem(
                    product_id, product_name, product_price, product_qty
                )
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
                product = InventoryItem(
                    product_id, product_name, product_price, product_qty
                )
                inventory[product_id] = product
            return inventory
        except Exception as error:
            print(f"Error displaying inventory from database: {error}")
            return {}
        finally:
            close_connection(con, cur)