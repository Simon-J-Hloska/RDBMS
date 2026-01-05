from src.dao.customer_dao import CustomerDAO
from src.dao.payment_dao import PaymentDAO
from src.model.customer import Customer


class CustomerRepository:
    def __init__(self):
        self.dao = CustomerDAO()
        self.payment_dao = PaymentDAO()

    def save(self, customer):
        """
        :param customer: Customer object
        :return: Customer ID
        """
        return self.dao.create(
            customer.first_name,
            customer.last_name,
            customer.email,
            customer.phone
        )

    def find_by_id(self, customer_id):
        """
        :param customer_id: Customer ID
        :return: Customer object or None
        """
        data = self.dao.read(customer_id)
        if data:
            return Customer(
                customer_id=data[0],
                first_name=data[1],
                last_name=data[2],
                email=data[3],
                phone=data[4],
                created_at=data[5]
            )
        return None

    def find_by_email(self, email):
        """
        :param email: User's email
        :return: Customer object or None
        """
        data = self.dao.find_by_email(email)
        if data:
            return Customer(
                customer_id=data[0],
                first_name=data[1],
                last_name=data[2],
                email=data[3],
                phone=data[4],
                created_at=data[5]
            )
        return None

    def find_all(self):
        """
        :return: List of Customer objects
        """
        results = self.dao.read_all()
        return [
            Customer(
                customer_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                phone=row[4],
                created_at=row[5]
            )
            for row in results
        ]

    def update_status(self, payment_id, status):
        """
        :param payment_id: Payment ID
        :param status: New status
        :return: Number of affected rows
        """
        return self.payment_dao.update_status(payment_id, status)

    def update(self, customer):
        """
        :param customer: customer object
        :return: Number of affected rows
        """
        return self.dao.update(customer.first_name, customer.last_name,
                               customer.email, customer.phone, customer.created_at)

    def delete(self, customer):
        """
        :param customer:
        :return: Number of affected rows
        """
        return self.dao.delete(customer.customer_id)