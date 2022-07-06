from psycopg2 import connect, OperationalError, DatabaseError
from sys import exc_info

from lib.Adapter import Adapter


class Postgres(Adapter):
    error = (Exception, DatabaseError)

    def showException(self, err):
        """ Show psycopg2 exceptions """
        err_type, _, traceback = exc_info()
        line_n = traceback.tb_lineno

        print("\npsycopg2 ERROR:", err, "on line number:", line_n)
        print("psycopg2 traceback:", traceback, "-- type:", err_type)

    def connect(self, **conn_params_dic) -> any:
        """ Connect to PostgreSQL database server """
        if len(conn_params_dic.keys()) != 4:
            conn_params_dic = {
                "host": "localhost",
                "database": "models",
                "user": "postgres",
                "password": "6O22i408r&"
            }

        try:
            self.conn = connect(**conn_params_dic)
        except OperationalError as err:
            self.showException(err)
            raise ConnectionError("Error accessing database server")

        return self.conn
        
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
        exists = False

        with self.conn.cursor() as cursor:
            try:
                cursor.execute(f"""
                    SELECT EXISTS(
                        SELECT * 
                        FROM information_schema.tables 
                        WHERE 
                        table_name = '{tableName}'
                    );
                """)
                exists = bool(cursor.fetchone()[0])
            except self.error as err:
                exists = False
                self.showException(err)
            finally:
                return exists