from src.repository.order_repository import OrderRepository
from src.repository.product_repository import ProductRepository
from src.repository.customer_repository import CustomerRepository


class ReportService:
    def __init__(self):
        self.order_repository = OrderRepository()
        self.product_repository = ProductRepository()
        self.customer_repository = CustomerRepository()

    def get_sales_summary(self):
        """
        :return: Dictionary with sales summary
        """
        orders = self.order_repository.find_all()

        total_revenue = sum(order.total_amount for order in orders if order.status != 'cancelled')
        completed_orders = len([o for o in orders if o.status == 'delivered'])
        pending_orders = len([o for o in orders if o.status == 'pending'])

        return {
            'total_orders': len(orders),
            'completed_orders': completed_orders,
            'pending_orders': pending_orders,
            'total_revenue': total_revenue
        }

    def get_low_stock_products(self, threshold=10):
        """
        :param threshold: Stock quantity threshold
        :return: List of products with low stock
        """
        products = self.product_repository.find_all()
        return [p for p in products if p.stock_quantity < threshold]

    def get_customer_statistics(self, customer_id):
        """
        :param customer_id: Customer ID
        :return: Dictionary with customer statistics
        """
        orders = self.order_repository.find_by_customer(customer_id)

        total_spent = sum(order.total_amount for order in orders if order.status != 'cancelled')
        completed_orders = len([o for o in orders if o.status == 'delivered'])

        return {
            'total_orders': len(orders),
            'completed_orders': completed_orders,
            'total_spent': total_spent
        }

