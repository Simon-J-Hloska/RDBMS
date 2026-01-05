from src.database.database_connection import DatabaseConnection


class CustomerDAO:
    def __init__(self):
        self.db = DatabaseConnection()
        self.connection = self.db.get_connection()

    def create(self, first_name, last_name, email, phone):
        """
        :param first_name: Customer first name
        :param last_name: Customer last name
        :param email: Customer email
        :param phone: Customer phone
        :return: Last inserted customer ID
        """
        cursor = self.connection.cursor()
        query = """
            INSERT INTO customers (first_name, last_name, email, phone)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, email, phone))
        self.connection.commit()
        customer_id = cursor.lastrowid
        cursor.close()
        return customer_id

    def read(self, customer_id):
        """
        :param customer_id: Customer ID
        :return: Customer data as tuple
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM customers WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def read_all(self):
        """
        :return: List of all customers
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM customers"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def update(self, customer_id, first_name, last_name, email, phone):
        """
        :param customer_id: Customer ID
        :param first_name: Customer first name
        :param last_name: Customer last name
        :param email: Customer email
        :param phone: Customer phone
        :return: Number of affected rows
        """
        cursor = self.connection.cursor()
        query = """
            UPDATE customers 
            SET first_name = %s, last_name = %s, email = %s, phone = %s
            WHERE customer_id = %s
        """
        cursor.execute(query, (first_name, last_name, email, phone, customer_id))
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

    def delete(self, customer_id):
        """
        :param customer_id: Customer ID
        :return: Number of affected rows
        """
        cursor = self.connection.cursor()
        query = "DELETE FROM customers WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

    def find_by_email(self, email):
        """
        :param email: Customer email
        :return: Customer data as tuple
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM customers WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def find_by_id(self, Customer_id):
        """
        :param Customer_id: Customer id
        :return: Customer data
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM customers WHERE customer_id = %s"
        cursor.execute(query, (Customer_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

