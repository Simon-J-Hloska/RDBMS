from datetime import datetime


class Order:
    def __init__(self, order_id=None, customer_id=None, order_date=None,
                 status='pending', total_amount=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_date = order_date or datetime.now()
        self.status = status
        self.total_amount = total_amount

    def to_dict(self):
        """
        :return: Dictionary representation of order
        """
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'order_date': self.order_date,
            'status': self.status,
            'total_amount': self.total_amount
        }

