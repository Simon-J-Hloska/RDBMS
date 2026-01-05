import mysql.connector
from src.config.configuration_loader import ConfigurationLoader


class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._connection is None:
            config = ConfigurationLoader()
            self._connection = mysql.connector.connect(
                host=config.get('database', 'host'),
                port=config.get_int('database', 'port'),
                database=config.get('database', 'database'),
                user=config.get('database', 'user'),
                password=config.get('database', 'password')
            )

    def get_connection(self):
        """
        :return: Active database connection
        """
        if not self._connection.is_connected():
            self._connection.reconnect()
        return self._connection

    def close(self):
        """
        :return: None
        """
        if self._connection and self._connection.is_connected():
            self._connection.close()

