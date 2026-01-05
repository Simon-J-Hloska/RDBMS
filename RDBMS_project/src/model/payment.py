from datetime import datetime


class Payment:
    def __init__(self, payment_id=None, order_id=None, payment_date=None,
                 amount=None, payment_method=None, status='pending'):
        self.payment_id = payment_id
        self.order_id = order_id
        self.payment_date = payment_date or datetime.now()
        self.amount = amount
        self.payment_method = payment_method
        self.status = status

    def to_dict(self):
        """
        :return: Dictionary representation of payment
        """
        return {
            'payment_id': self.payment_id,
            'order_id': self.order_id,
            'payment_date': self.payment_date,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'status': self.status
        }

