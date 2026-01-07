from pathlib import Path

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
        self.config = ConfigurationLoader()
        if self._connection is None:
            self._connection = self._create_connection()


    def _create_connection(self):
        db_name = self.config.get('database', 'database')
        _connection = mysql.connector.connect(
            host=self.config.get('database', 'host'),
            port=self.config.get_int('database', 'port'),
            user=self.config.get('database', 'user'),
            password=self.config.get('database', 'password')
        )
        cursor = _connection.cursor(buffered=True)
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s", (db_name,))
        db_exists = cursor.fetchone()
        if not db_exists:
            sql_path = Path("../../sql/db_query.sql")
            sql_content = sql_path.read_text(encoding="utf-8")
            cursor.execute(sql_content)
            _connection.commit()
            self._import_sample_data(cursor)
        cursor.close()
        _connection.close()

        return mysql.connector.connect(
            host=self.config.get('database', 'host'),
            port=self.config.get_int('database', 'port'),
            database=db_name,
            user=self.config.get('database', 'user'),
            password=self.config.get('database', 'password'),
        )

    def _import_sample_data(self, cursor):
        sql_path = Path("../../sql/sample_data.sql")
        sql_content = sql_path.read_text(encoding="utf-8")
        for statement in sql_content.split(';'):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
        self._connection.commit()

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

