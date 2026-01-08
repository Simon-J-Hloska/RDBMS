from RDBMS_project.src.repository.customer_repository import CustomerRepository
from RDBMS_project.src.model.customer import Customer
from RDBMS_project.src.utils.input_validator import InputValidator
from RDBMS_project.src.utils.error_handler import ErrorHandler


class CustomerService:
    def __init__(self):
        self.repository = CustomerRepository()

    def create_customer(self, first_name, last_name, email, phone):
        """
        :param first_name: First name
        :param last_name: Last name
        :param email: Email address
        :param phone: Phone number
        :return: Created customer ID
        """
        ErrorHandler.validate_and_raise(
            InputValidator.validate_not_empty(first_name),
            "Jméno nesmí být prázdné"
        )
        ErrorHandler.validate_and_raise(
            InputValidator.validate_not_empty(last_name),
            "Příjmení nesmí být prázdné"
        )
        ErrorHandler.validate_and_raise(
            InputValidator.validate_email(email),
            "Neplatný formát emailu"
        )
        ErrorHandler.validate_and_raise(
            InputValidator.validate_phone(phone),
            "Neplatný formát telefonu"
        )

        existing = self.repository.find_by_email(email)
        ErrorHandler.validate_and_raise(
            existing is None,
            "Zákazník s tímto emailem již existuje"
        )

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )
        return self.repository.save(customer)

    def get_customer(self, customer_id):
        """
        :param customer_id: Customer ID
        :return: Customer object or None
        """
        return self.repository.find_by_id(customer_id)

    def get_all_customers(self):
        """
        :return: List of all customers
        """
        return self.repository.find_all()

    def update_customer(self, customer_id, first_name, last_name, email, phone):
        """
        :param customer_id: Customer ID
        :param first_name: First name
        :param last_name: Last name
        :param email: Email address
        :param phone: Phone number
        :return: count of affected rows
        """
        ErrorHandler.validate_and_raise(
            InputValidator.validate_not_empty(first_name),
            "Jméno nesmí být prázdné"
        )
        ErrorHandler.validate_and_raise(
            InputValidator.validate_not_empty(last_name),
            "Příjmení nesmí být prázdné"
        )
        ErrorHandler.validate_and_raise(
            InputValidator.validate_email(email),
            "Neplatný formát emailu"
        )
        ErrorHandler.validate_and_raise(
            InputValidator.validate_phone(phone),
            "Neplatný formát telefonu"
        )

        customer = self.repository.find_by_id(customer_id)
        ErrorHandler.validate_and_raise(
            customer is not None,
            "Zákazník nebyl nalezen"
        )

        customer.first_name = first_name
        customer.last_name = last_name
        customer.email = email
        customer.phone = phone

        return self.repository.update(customer)

    def delete_customer(self, customer_id):
        """
        :param customer_id: Customer ID
        :return: Number of affected rows
        """
        customer = self.repository.find_by_id(customer_id)
        ErrorHandler.validate_and_raise(
            customer is not None,
            "Zákazník nebyl nalezen"
        )
        return self.repository.delete(customer_id)

