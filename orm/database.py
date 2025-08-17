import sqlite3

class Database:
    _connection = None
    _cursor = None
    _db_name = None

    @classmethod
    def connect(cls, db_name="orm.db"):
        if cls._connection is None:
            cls._db_name = db_name
            # ⚡ تغییر مهم: اجازه استفاده در threadهای مختلف
            cls._connection = sqlite3.connect(db_name, check_same_thread=False)
            cls._connection.row_factory = sqlite3.Row
            cls._cursor = cls._connection.cursor()
        return cls._connection, cls._cursor

    @classmethod
    def execute(cls, query, params=None):
        conn, cursor = cls.connect()
        if params is None:
            params = []
        cursor.execute(query, params)
        conn.commit()
        return cursor

    @classmethod
    def executemany(cls, query, seq_of_params):
        conn, cursor = cls.connect()
        cursor.executemany(query, seq_of_params)
        conn.commit()
        return cursor

    @classmethod
    def close(cls):
        if cls._connection:
            cls._connection.close()
            cls._connection = None
            cls._cursor = None
            cls._db_name = None
