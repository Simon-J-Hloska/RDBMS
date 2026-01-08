from RDBMS_project.src.dao.product_dao import ProductDAO
from RDBMS_project.src.model.product import Product


class ProductRepository:
    def __init__(self):
        self.dao = ProductDAO()

    @staticmethod
    def check_is_not_null(product):
        for value in product:
            if value.trim == "" or value is not None:
                raise TypeError('pole nesmí být prázdné')

    def save(self, product):
        """
        :param product: Product object
        :return: Product ID
        """
        self.check_is_not_null(product)
        if product.price < 0:
            raise ValueError("cena musí být víc než nula")
        if product.stock_quantity <= 0:
            raise ValueError("musí být alespoň 1 produkt na skladě")
        return self.dao.create(
            product.name,
            product.description,
            product.price,
            product.stock_quantity
        )

    def find_by_id(self, product_id):
        """
        :param product_id: Product ID
        :return: Product object or None
        """
        data = self.dao.read(product_id)
        if data:
            return Product(
                product_id=data[0],
                name=data[1],
                description=data[2],
                price=data[3],
                stock_quantity=data[4],
                created_at=data[5]
            )
        return None

    def find_all(self):
        """
        :return: List of Product objects
        """
        results = self.dao.read_all()
        return [
            Product(
                product_id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                stock_quantity=row[4],
                created_at=row[5]
            )
            for row in results
        ]

    def update(self, product):
        """
        :param product: Product object
        :return: Number of affected rows
        """
        self.check_is_not_null(product)
        if product.price < 0:
            raise ValueError("cena musí být víc než nula")
        if product.stock_quantity <= 0:
            raise ValueError("musí být alespoň 1 produkt na skladě")
        return self.dao.update(
            product.product_id,
            product.name,
            product.description,
            product.price,
            product.stock_quantity
        )

    def delete(self, product_id):
        """
        :param product_id: Product ID
        :return: Number of affected rows
        """
        return self.dao.delete(product_id)

    def update_stock(self, product_id, quantity_change):
        self.check_is_not_null(quantity_change)
        if quantity_change <= 0:
            raise ValueError("musí být alespoň 1 produkt na skladě, popř. odstraňte produkt")
        """
        :param product_id: Product ID
        :param quantity_change: Quantity to add or subtract
        :return: Number of affected rows
        """
        return self.dao.update_stock(product_id, quantity_change)

