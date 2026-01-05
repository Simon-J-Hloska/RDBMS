from src.database.database_connection import DatabaseConnection


class OrderItemDAO:
    def __init__(self):
        self.db = DatabaseConnection()
        self.connection = self.db.get_connection()

    def create(self, order_id, product_id, quantity, unit_price, subtotal):
        """
        :param order_id: Order ID
        :param product_id: Product ID
        :param quantity: Quantity
        :param unit_price: Unit price
        :param subtotal: Subtotal
        :return: Last inserted order item ID
        """
        cursor = self.connection.cursor()
        query = """
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (order_id, product_id, quantity, unit_price, subtotal))
        self.connection.commit()
        order_item_id = cursor.lastrowid
        cursor.close()
        return order_item_id

    def read(self, order_item_id):
        """
        :param order_item_id: Order item ID
        :return: Order item data as tuple
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM order_items WHERE order_item_id = %s"
        cursor.execute(query, (order_item_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def find_by_order(self, order_id):
        """
        :param order_id: Order ID
        :return: List of order items
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM order_items WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        results = cursor.fetchall()
        cursor.close()
        return results

    def delete_by_order(self, order_id):
        """
        :param order_id: Order ID
        :return: Number of affected rows
        """
        cursor = self.connection.cursor()
        query = "DELETE FROM order_items WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

