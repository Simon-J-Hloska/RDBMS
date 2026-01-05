from datetime import datetime


class Customer:
    def __init__(self, customer_id=None, first_name=None, last_name=None,
                 email=None, phone=None, created_at=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        """
        :return: Dictionary representation of customer
        """
        return {
            'customer_id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at
        }

