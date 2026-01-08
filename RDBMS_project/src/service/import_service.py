import csv
import json
from pathlib import Path

from RDBMS_project.src.repository.customer_repository import CustomerRepository
from RDBMS_project.src.repository.product_repository import ProductRepository
from RDBMS_project.src.model.customer import Customer
from RDBMS_project.src.model.product import Product
from RDBMS_project.src.database.transaction_manager import TransactionManager
from RDBMS_project.src.utils.input_validator import InputValidator
from RDBMS_project.src.utils.error_handler import ErrorHandler


class ImportService:
    def __init__(self):
        self.customer_repository = CustomerRepository()
        self.product_repository = ProductRepository()
        self.transaction_manager = TransactionManager()

    def import_customers_from_csv(self, filename):
        """
        :param filename: Path to CSV file
        :return: Number of imported customers
        """
        customers = []
        base_dir = Path(__file__).resolve().parent
        data_path = base_dir / "../../data/{filename}".format(filename=filename)

        with open(data_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ErrorHandler.validate_and_raise(
                    InputValidator.validate_email(row['email']),
                    f"Neplatný email: {row['email']}"
                )
                ErrorHandler.validate_and_raise(
                    InputValidator.validate_phone(row['phone']),
                    f"Neplatný telefon: {row['phone']}"
                )

                customer = Customer(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    phone=row['phone']
                )
                customers.append(customer)

        def import_transaction():
            count = 0
            for cstomer in customers:
                self.customer_repository.save(cstomer)
                count += 1
            return count

        return self.transaction_manager.execute_in_transaction([import_transaction])[0]

    def import_products_from_json(self, filename):
        """
        :param filename: Path to JSON file
        :return: Number of imported products
        """
        base_dir = Path(__file__).resolve().parent
        data_path = base_dir / "../../data/{filename}".format(filename=filename)

        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        products = []
        for item in data:
            ErrorHandler.validate_and_raise(
                InputValidator.validate_positive_number(item['price']),
                f"Neplatná cena: {item['price']}"
            )
            ErrorHandler.validate_and_raise(
                InputValidator.validate_positive_number(item['stock_quantity']),
                f"Neplatné množství: {item['stock_quantity']}"
            )

            product = Product(
                name=item['name'],
                description=item.get('description', ''),
                price=float(item['price']),
                stock_quantity=int(item['stock_quantity'])
            )
            products.append(product)

        def import_transaction():
            count = 0
            for prod in products:
                self.product_repository.save(prod)
                count += 1
            return count
        return self.transaction_manager.execute_in_transaction([import_transaction])[0]

