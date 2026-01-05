from src.database.database_connection import DatabaseConnection


class ProductDAO:
    def __init__(self):
        self.db = DatabaseConnection()
        self.connection = self.db.get_connection()

    def create(self, name, description, price, stock_quantity):
        """
        :param name: Product name
        :param description: Product description
        :param price: Product price
        :param stock_quantity: Stock quantity
        :return: Last inserted product ID
        """
        cursor = self.connection.cursor()
        query = """
            INSERT INTO products (name, description, price, stock_quantity)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, description, price, stock_quantity))
        self.connection.commit()
        product_id = cursor.lastrowid
        cursor.close()
        return product_id

    def read(self, product_id):
        """
        :param product_id: Product ID
        :return: Product data as tuple
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM products WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def read_all(self):
        """
        :return: List of all products
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM products"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def update(self, product_id, name, description, price, stock_quantity):
        """
        :param product_id: Product ID
        :param name: Product name
        :param description: Product description
        :param price: Product price
        :param stock_quantity: Stock quantity
        :return: Number of affected rows
        """
        cursor = self.connection.cursor()
        query = """
            UPDATE products 
            SET name = %s, description = %s, price = %s, stock_quantity = %s
            WHERE product_id = %s
        """
        cursor.execute(query, (name, description, price, stock_quantity, product_id))
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

    def delete(self, product_id):
        """
        :param product_id: Product ID
        :return: Number of affected rows
        """
        cursor = self.connection.cursor()
        query = "DELETE FROM products WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

    def update_stock(self, product_id, quantity_change):
        """
        :param product_id: Product ID
        :param quantity_change: Quantity to add or subtract
        :return: Number of affected rows
        """
        cursor = self.connection.cursor()
        query = """
            UPDATE products 
            SET stock_quantity = stock_quantity + %s
            WHERE product_id = %s
        """
        cursor.execute(query, (quantity_change, product_id))
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

