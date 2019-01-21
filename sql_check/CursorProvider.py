from mysql import connector

import Singleton


class CursorProvider(metaclass=Singleton):

    def __init__(self):
        self.connection = connector.connect(
            host="127.0.0.1",
            user="root",
            passwd=""
        )

    def __del__(self):
        if self.connection.is_connected():
            self.connection.close()

    def cursor(self):
        return self.connection.cursor()
