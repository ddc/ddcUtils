# -*- encoding: utf-8 -*-
import sys
import sqlalchemy as sa
from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.orm import Session
from ..exceptions import get_exception


class DBSqlite:
    """
    Class to handle sqlite databases

        database = DBSqlite(DATABASE_FILE_PATH)
        with database.session() as session:
            do your stuff here

    """
    def __init__(self, db_file_path: str, batch_size=100, echo=False):
        self.file = db_file_path
        self.batch_size = batch_size
        self.echo = echo

    def engine(self):
        try:
            engine = create_engine(f"sqlite:///{self.file}", future=True, echo=self.echo).\
                execution_options(stream_results=self.echo, isolation_level="AUTOCOMMIT")

            @sa.event.listens_for(engine, "before_cursor_execute")
            def receive_before_cursor_execute(conn,
                                              cursor,
                                              statement,
                                              params,
                                              context,
                                              executemany):
                cursor.arraysize = self.batch_size
            return engine
        except Exception as e:
            sys.stderr.write(f"Unable to Create Database Engine: {get_exception(e)}")
            return None

    def session(self, engine: Engine = None) -> Session | None:
        _engine = engine or self.engine()
        if _engine is None:
            sys.stderr.write("Unable to Create Database Session: Empty Engine")
            return None
        session = Session(bind=_engine)
        return session
