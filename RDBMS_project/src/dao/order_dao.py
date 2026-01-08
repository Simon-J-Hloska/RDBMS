from RDBMS_project.src.database.database_connection import DatabaseConnection


class OrderDAO:
    def __init__(self):
        self.db = DatabaseConnection()
        self.connection = self.db.get_connection()

    def create(self, customer_id, status, total_amount):
        """
        :param customer_id: Customer ID
        :param status: Order status
        :param total_amount: Total amount
        :return: Last inserted order ID
        """
        cursor = self.connection.cursor()
        query = """
            INSERT INTO orders (customer_id, status, total_amount)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (customer_id, status, total_amount))
        self.connection.commit()
        order_id = cursor.lastrowid
        cursor.close()
        return order_id

    def read(self, order_id):
        """
        :param order_id: Order ID
        :return: Order data as tuple
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM orders WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def read_all(self):
        """
        :return: List of all orders
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM orders"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def update_status(self, order_id, status):
        """
        :param order_id: Order ID
        :param status: New status
        :return: Number of affected rows
        """
        cursor = self.connection.cursor()
        query = "UPDATE orders SET status = %s WHERE order_id = %s"
        cursor.execute(query, (status, order_id))
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

    def delete(self, order_id):
        """
        :param order_id: Order ID
        :return: Number of affected rows
        """
        cursor = self.connection.cursor()
        query = "DELETE FROM orders WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

    def find_by_customer(self, customer_id):
        """
        :param customer_id: Customer ID
        :return: List of orders for customer
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM orders WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        results = cursor.fetchall()
        cursor.close()
        return results

