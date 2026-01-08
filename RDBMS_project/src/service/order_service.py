from RDBMS_project.src.repository.order_repository import OrderRepository
from RDBMS_project.src.repository.product_repository import ProductRepository
from RDBMS_project.src.repository.customer_repository import CustomerRepository
from RDBMS_project.src.repository.payment_repository import PaymentRepository
from RDBMS_project.src.model.order import Order
from RDBMS_project.src.model.order_item import OrderItem
from RDBMS_project.src.model.payment import Payment
from RDBMS_project.src.database.transaction_manager import TransactionManager
from RDBMS_project.src.utils.error_handler import ErrorHandler


class OrderService:
    def __init__(self):
        self.order_repository = OrderRepository()
        self.product_repository = ProductRepository()
        self.customer_repository = CustomerRepository()
        self.payment_repository = PaymentRepository()
        self.transaction_manager = TransactionManager()

    def create_order(self, customer_id, items, payment_method):
        """
        :param customer_id: Customer ID
        :param items: List of tuples (product_id, quantity)
        :param payment_method: Payment method
        :return: Created order ID
        """
        customer = self.customer_repository.find_by_id(customer_id)
        ErrorHandler.validate_and_raise(
            customer is not None,
            "Zákazník nebyl nalezen"
        )

        ErrorHandler.validate_and_raise(
            len(items) > 0,
            "Objednávka musí obsahovat alespoň jednu položku"
        )

        total_amount = 0
        order_items_data = []

        for product_id, quantity in items:
            product = self.product_repository.find_by_id(product_id)
            ErrorHandler.validate_and_raise(
                product is not None,
                f"Produkt s ID {product_id} nebyl nalezen"
            )
            ErrorHandler.validate_and_raise(
                product.stock_quantity >= quantity,
                f"Nedostatečné množství produktu {product.name} na skladě"
            )

            subtotal = product.price * quantity
            total_amount += subtotal
            order_items_data.append({
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': product.price,
                'subtotal': subtotal
            })

        def create_order_transaction():
            order = Order(
                customer_id=customer_id,
                status='pending',
                total_amount=total_amount
            )
            order_id = self.order_repository.save(order)

            for item_data in order_items_data:
                order_item = OrderItem(
                    order_id=order_id,
                    product_id=item_data['product_id'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    subtotal=item_data['subtotal']
                )
                self.order_repository.save_order_item(order_item)
                self.product_repository.update_stock(
                    item_data['product_id'],
                    -item_data['quantity']
                )

            payment = Payment(
                order_id=order_id,
                amount=total_amount,
                payment_method=payment_method,
                status='pending'
            )
            self.payment_repository.save(payment)

            return order_id

        return self.transaction_manager.execute_in_transaction([create_order_transaction])[0]

    def get_order(self, order_id):
        """
        :param order_id: Order ID
        :return: Order object or None
        """
        return self.order_repository.find_by_id(order_id)

    def get_order_details(self, order_id):
        """
        :param order_id: Order ID
        :return: Dictionary with order details
        """
        order = self.order_repository.find_by_id(order_id)
        if not order:
            return None

        items = self.order_repository.find_order_items(order_id)
        customer = self.customer_repository.find_by_id(order.customer_id)
        payments = self.payment_repository.find_by_order(order_id)

        return {
            'order': order,
            'customer': customer,
            'items': items,
            'payments': payments
        }

    def get_all_orders(self):
        """
        :return: List of all orders
        """
        return self.order_repository.find_all()

    def update_order_status(self, order_id, status):
        """
        :param order_id: Order ID
        :param status: New status
        :return: Number of affected rows
        """
        valid_statuses = ['pending','paid','shipped','cancelled']
        ErrorHandler.validate_and_raise(
            status in valid_statuses,
            f"Neplatný status. Povolené hodnoty: {', '.join(valid_statuses)}"
        )

        order = self.order_repository.find_by_id(order_id)
        ErrorHandler.validate_and_raise(
            order is not None,
            "Objednávka nebyla nalezena"
        )

        return self.order_repository.update_status(order_id, status)

    def cancel_order(self, order_id):
        """
        :param order_id: Order ID
        :return: None
        """
        order = self.order_repository.find_by_id(order_id)
        ErrorHandler.validate_and_raise(
            order is not None,
            "Objednávka nebyla nalezena"
        )

        ErrorHandler.validate_and_raise(
            order.status == 'pending',
            "Lze zrušit pouze objednávky ve stavu 'pending'"
        )

        def cancel_transaction():
            items = self.order_repository.find_order_items(order_id)
            for item in items:
                self.product_repository.update_stock(
                    item.product_id,
                    item.quantity
                )
            self.order_repository.update_status(order_id, 'cancelled')

        self.transaction_manager.execute_in_transaction([cancel_transaction])

    def get_customer_orders(self, customer_id):
        """
        :param customer_id: Customer ID
        :return: List of orders for customer
        """
        return self.order_repository.find_by_customer(customer_id)

