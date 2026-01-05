from src.database.database_connection import DatabaseConnection


class TransactionManager:
    def __init__(self):
        self.db = DatabaseConnection()
        self.connection = self.db.get_connection()
        self.connection.autocommit = False
        self._in_transaction = False

    def begin(self):
        """
        :return: None
        """
        if self._in_transaction:
            raise RuntimeError("Transaction already started")
        self.connection.start_transaction()
        self._in_transaction = True

    def commit(self):
        """
        :return: None
        """
        self.connection.commit()
        self._in_transaction = False

    def rollback(self):
        """
        :return: None
        """
        self.connection.rollback()
        self._in_transaction = False

    def execute_in_transaction(self, operation):
        self.begin()
        try:
            result = operation()
            self.commit()
            return result
        except:
            self.rollback()
            raise

