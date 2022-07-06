from lib.Adapter import Adapter

import sqlite3
from sqlite3 import Error


class Sqlite3(Adapter):
    error = (Error)

    def showException(self, err):
        print("Error: %s" % err)

    def connect(self, path):
        """ create a database connection to the SQLite database
            specified by the path

        Parameters
        ----------
            path: database file
        Returns
        -------
            Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(path)
        except Error as e:
            print(e)

        return conn

    def tableExist(self, tableName: str) -> bool:
        """ Check if table exists

        Parameters
        ----------
            tableName: str()  Default = ""
                model present in self.tables.
                If None, will search all tables.

        Returns
        -------
            bool()
        """
        exist = False
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"""
                PRAGMA table_info('{tableName}')
            """)
            exists = cursor.fetchone() != None
        except self.error as err:
            exists = False
            self.showException(err)
        finally:
            cursor.close()
            return exists
