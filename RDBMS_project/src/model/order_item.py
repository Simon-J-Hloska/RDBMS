class OrderItem:
    def __init__(self, order_item_id=None, order_id=None, product_id=None,
                 quantity=None, unit_price=None, subtotal=None):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = subtotal

    def to_dict(self):
        """
        :return: Dictionary representation of order item
        """
        return {
            'order_item_id': self.order_item_id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'subtotal': self.subtotal
        }

