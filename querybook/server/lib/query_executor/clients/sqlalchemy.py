import sqlalchemy

from lib.query_executor.base_client import ClientBaseClass, CursorBaseClass


class SqlAlchemyClient(ClientBaseClass):
    def __init__(self, connection_string=None, proxy_user=None, *args, **kwargs):
        self._engine = sqlalchemy.create_engine(connection_string)
        super(SqlAlchemyClient, self).__init__()

    def __del__(self):
        self._engine.dispose()

    def cursor(self) -> CursorBaseClass:
        return SqlAlchemyCursor(engine=self._engine)


class SqlAlchemyCursor(CursorBaseClass):
    def __init__(self, engine):
        self._connection = engine.connect()

    def __del__(self):
        if self._connection:
            self._connection.close()

    def run(self, query):
        self._cursor = self._connection.execute(sqlalchemy.sql.text(query))

    def cancel(self):
        # Can't cancel (yet)
        pass

    def poll(self):
        # Query should immediately start to block after
        # run, so when it gets to poll it is already
        # finished
        return True

    def get_one_row(self):
        return list(self._cursor.fetchone())

    def get_n_rows(self, n: int):
        return [list(row) for row in self._cursor.fetchmany(size=n)]

    def get_columns(self):
        return self._cursor.keys()
