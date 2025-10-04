import pymysql
from pymysql import Connection
import logging

from app.core.config import DB_CONFIG

logging.basicConfig(level=logging.INFO)

class DB_CONN:
    _conn: Connection = None
    _cursor:pymysql.cursors.DictCursor = None

    def __init__(self):
        logging.info(" DB CONNECTING ▷▷▶ ")
        conn_string = DB_CONFIG["conn_string"]
        timeout = 10
        try:
            self._conn = pymysql.connect(
                charset="utf8mb4",
                connect_timeout=timeout,
                cursorclass=pymysql.cursors.DictCursor,
                read_timeout=timeout,
                write_timeout=timeout,
                host=conn_string.get("host"),
                port=conn_string.get("port"),
                user=conn_string.get("user"),
                password=conn_string.get("password"),
                db=conn_string.get("database")
            )
            logging.info("\t ✅::DB CONNECTION SUCCESSFUL::")

        except pymysql.DatabaseError as err:
            logging.error(f"\t ❌:: DB CONNECTION FAILED :: Database Error :: {err.args}")
            raise err

        except pymysql.Error as err:
            logging.error(f"\t ❌:: DB CONNECTION FAILED :: Connection Error :: {err.args}")
            raise err

        except Exception as err:
            logging.error(f"\t ❌:: DB CONNECTION FAILED :: Something went wrong :: {err.args}")
            raise err

    @property
    def cursor(self):
        if self._cursor is None and self._conn:
            self._cursor = self._conn.cursor()
        return self._cursor

    @cursor.deleter
    def cursor(self):
        if self._cursor:
            self._cursor.close()
            self._cursor = None

    def close(self):
        if self._cursor:
            self._cursor.close()
        if self._conn:
            logging.info(msg='DB CONNECTION CLOSED::')
            self._conn.close()

    def commit(self):
        if self._conn:
            self._conn.commit()
            logging.info(msg='Latest COMMIT SUCCESSFUL::')
        else:
            logging.warning("No active connection available")

    def reconnect(self):
        self.close()
        self.__init__()

