import re
from src.dao.customer_dao import CustomerDAO


class InputValidator:
    def __init__(self):
        self.dao = CustomerDAO()

    @staticmethod
    def validate_email(email):
        """
        :param email: Email address
        :return: True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        """
        :param phone: Phone number
        :return: True if valid, False otherwise
        """
        pattern = r'^(\+420\s?)?(\d{3}\s?){2}\d{3}$'
        return re.match(pattern, phone) is not None

    @staticmethod
    def validate_not_empty(name):
        """
        :param name: users Name
        :return: True if valid, False otherwise
        """
        return bool(name and name.strip())

    @staticmethod
    def validate_positive_number(value):
        """
        :param value: Numeric value
        :return: True if value is a positive number (> 0), False otherwise
        """
        if isinstance(value, (int, float)):
            return bool(value > 0)
        else:
            return False



