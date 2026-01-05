from src.dao.payment_dao import PaymentDAO
from src.model.payment import Payment


class PaymentRepository:
    def __init__(self):
        self.dao = PaymentDAO()

    def save(self, payment):
        """
        :param payment: Payment object
        :return: Payment ID
        """
        return self.dao.create(
            payment.order_id,
            payment.amount,
            payment.payment_method,
            payment.status
        )

    def find_by_id(self, payment_id):
        """
        :param payment_id: Payment ID
        :return: Payment object or None
        """
        data = self.dao.read(payment_id)
        if data:
            return Payment(
                payment_id=data[0],
                order_id=data[1],
                payment_date=data[2],
                amount=data[3],
                payment_method=data[4],
                status=data[5]
            )
        return None

    def find_by_order(self, order_id):
        """
        :param order_id: Order ID
        :return: List of Payment objects
        """
        results = self.dao.find_by_order(order_id)
        return [
            Payment(
                payment_id=results[0],
                order_id=results[1],
                payment_date=results[2],
                amount=results[3],
                payment_method=results[4],
                status=results[5]
            )]


    @staticmethod
    def validate_positive_number(value):
        """
        :param value: Numeric value
        :return: True if positive, False otherwise
        """
        try:
            return float(value) > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_positive_integer(value):
        """
        :param value: Integer value
        :return: True if positive integer, False otherwise
        """
        try:
            return 0 < int(value) == float(value)
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_not_empty(value):
        """
        :param value: String value
        :return: True if not empty, False otherwise
        """
        return value is not None and str(value).strip() != ''

