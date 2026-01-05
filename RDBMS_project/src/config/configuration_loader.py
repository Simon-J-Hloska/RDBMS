import configparser
import os


class ConfigurationLoader:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self._config = configparser.ConfigParser()
            config_path = os.path.join(os.path.dirname(__file__), 'app_config.ini')
            self._config.read(config_path)

    def get(self, section, key):
        """
        :param section: Configuration section name
        :param key: Configuration key
        :return: Configuration value
        """
        return self._config.get(section, key)

    def get_int(self, section, key):
        """
        :param section: Configuration section name
        :param key: Configuration key
        :return: Configuration value as integer
        """
        return self._config.getint(section, key)

