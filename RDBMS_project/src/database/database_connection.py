from pathlib import Path

import mysql.connector
from RDBMS_project.src.config.configuration_loader import ConfigurationLoader


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
        _connection = mysql.connector.connect(
            host=self.config.get('database', 'host'),
            port=self.config.get_int('database', 'port'),
            user=self.config.get('database', 'user'),
            password=self.config.get('database', 'password')
        )
        cursor = _connection.cursor(buffered=True)
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
                       (self.config.get('database', 'database'),))
        db_exists = cursor.fetchone()
        if not db_exists:
            self._import_data(cursor, "db_query.sql")
            cursor.close()
            _connection.close()
            _connection = self._create_db_connection()
            cursor = _connection.cursor(buffered=True)
            self._import_data(cursor, "sample_data.sql")
            _connection.commit()
        cursor.close()
        _connection.close()
        return self._create_db_connection()

    def _create_db_connection(self):
        return mysql.connector.connect(
            host=self.config.get('database', 'host'),
            port=self.config.get_int('database', 'port'),
            database=self.config.get('database', 'database'),
            user=self.config.get('database', 'user'),
            password=self.config.get('database', 'password'),
            autocommit=False
        )

    @staticmethod
    def _import_data(cursor, filename):
        base_dir = Path(__file__).resolve().parent
        sql_path = base_dir / "../../sql/{filename}".format(filename=filename)
        sql_content = sql_path.read_text(encoding="utf-8")
        if sql_content.strip() == "":
            return
        for statement in sql_content.split(';'):
            stmt = statement.strip()
            print(stmt)
            if stmt:
                cursor.execute(stmt)

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

