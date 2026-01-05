from datetime import datetime


class Product:
    def __init__(self, product_id=None, name=None, description=None,
                 price=None, stock_quantity=None, created_at=None):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        """
        :return: Dictionary representation of product
        """
        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock_quantity': self.stock_quantity,
            'created_at': self.created_at
        }

