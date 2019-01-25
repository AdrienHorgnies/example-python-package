import getpass

import yaml
from mysql import connector

from Singleton import Singleton


class CursorProvider(metaclass=Singleton):

    def __init__(self):
        with open("application.yml", "r") as config_file:
            config = yaml.load(config_file)

        host = config["mysql"]["host"]
        user = config["mysql"]["user"]

        self.connection = connector.connect(
            host=host,
            user=user,
            passwd=getpass.getpass("Password for {user}@{host}: ".format(user=user, host=host))
        )

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def cursor(self):
        return self.connection.cursor()
