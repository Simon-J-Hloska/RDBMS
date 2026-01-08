from RDBMS_project.src.database.database_connection import DatabaseConnection


class PaymentDAO:
    def __init__(self):
        self.db = DatabaseConnection()
        self.connection = self.db.get_connection()

    def create(self, order_id, amount, payment_method, status):
        """
        :param order_id: Order ID
        :param amount: Payment amount
        :param payment_method: Payment method
        :param status: Payment status
        :return: Last inserted payment ID
        """
        cursor = self.connection.cursor()
        query = """
            INSERT INTO payments (order_id, amount, payment_method, status)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (order_id, amount, payment_method, status))
        self.connection.commit()
        payment_id = cursor.lastrowid
        cursor.close()
        return payment_id

    def read(self, payment_id):
        """
        :param payment_id: Payment ID
        :return: Payment data as tuple
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM payments WHERE payment_id = %s"
        cursor.execute(query, (payment_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def find_by_order(self, order_id):
        """
        :param order_id: Order ID
        :return: List of payments for order
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM payments WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        results = cursor.fetchall()
        cursor.close()
        return results

    def update_status(self, payment_id, status):
        """
        :param payment_id: Payment ID
        :param status: New status
        :return: Number of affected rows
        """
        cursor = self.connection.cursor()
        query = "UPDATE payments SET status = %s WHERE payment_id = %s"
        cursor.execute(query, (status, payment_id))
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

