import yaml
from mysql import connector

import Singleton


class CursorProvider(metaclass=Singleton):

    def __init__(self):
        with open("application.yml", "r") as config_file:
            config = yaml.load(config_file)

        self.connection = connector.connect(
            host=config["mysql"]["host"],
            user=config["mysql"]["user"],
            passwd=""
        )

    def __del__(self):
        if self.connection.is_connected():
            self.connection.close()

    def cursor(self):
        return self.connection.cursor()
