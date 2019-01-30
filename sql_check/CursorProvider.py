import getpass

from mysql import connector

from Singleton import Singleton
from chest import Chest


class CursorProvider(metaclass=Singleton):

    def __init__(self):
        self.connection = connector.connect(
            host=Chest()["host"],
            user=Chest()["user"],
            passwd=getpass.getpass("Password for {user}@{host}: ".format(user=Chest()["user"], host=Chest()["host"]))
        )

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()

    def cursor(self):
        return self.connection.cursor()

    @staticmethod
    def add_arguments_to(parser):
        parser.add_argument("--host", required=True, help="MySQL Server host. Can be configured with mysql.host.",
                            conf_key="mysql.host")
        parser.add_argument("--user", required=True, help="MySQL Server user. Can be configured with mysql.user.",
                            conf_key="mysql.user")
