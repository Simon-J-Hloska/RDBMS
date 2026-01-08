from RDBMS_project.src.dao.order_dao import OrderDAO
from RDBMS_project.src.dao.order_item_dao import OrderItemDAO
from RDBMS_project.src.model.order import Order
from RDBMS_project.src.model.order_item import OrderItem


class OrderRepository:
    def __init__(self):
        self.order_dao = OrderDAO()
        self.order_item_dao = OrderItemDAO()

    def save(self, order):
        """
        :param order: Order object
        :return: Order ID
        """
        return self.order_dao.create(
            order.customer_id,
            order.status,
            order.total_amount
        )

    def find_by_id(self, order_id):
        """
        :param order_id: Order ID
        :return: Order object or None
        """
        data = self.order_dao.read(order_id)
        if data:
            return Order(
                order_id=data[0],
                customer_id=data[1],
                order_date=data[2],
                status=data[3],
                total_amount=data[4]
            )
        return None

    def find_all(self):
        """
        :return: List of Order objects
        """
        results = self.order_dao.read_all()
        return [
            Order(
                order_id=row[0],
                customer_id=row[1],
                order_date=row[2],
                status=row[3],
                total_amount=row[4]
            )
            for row in results
        ]

    def update_status(self, order_id, status):
        """
        :param order_id: Order ID
        :param status: New status
        :return: Number of affected rows
        """
        return self.order_dao.update_status(order_id, status)

    def delete(self, order_id):
        """
        :param order_id: Order ID
        :return: Number of affected rows
        """
        return self.order_dao.delete(order_id)

    def find_by_customer(self, customer_id):
        """
        :param customer_id: Customer ID
        :return: List of Order objects
        """
        results = self.order_dao.find_by_customer(customer_id)
        return [
            Order(
                order_id=row[0],
                customer_id=row[1],
                order_date=row[2],
                status=row[3],
                total_amount=row[4]
            )
            for row in results
        ]

    def save_order_item(self, order_item):
        """
        :param order_item: OrderItem object
        :return: Order item ID
        """
        return self.order_item_dao.create(
            order_item.order_id,
            order_item.product_id,
            order_item.quantity,
            order_item.unit_price,
            order_item.subtotal
        )

    def find_order_items(self, order_id):
        """
        :param order_id: Order ID
        :return: List of OrderItem objects
        """
        results = self.order_item_dao.find_by_order(order_id)
        return [
            OrderItem(
                order_item_id=row[0],
                order_id=row[1],
                product_id=row[2],
                quantity=row[3],
                unit_price=row[4],
                subtotal=row[5]
            )
            for row in results
        ]

