# -*- encoding: utf-8 -*-
import sys
import sqlalchemy as sa
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session
from ..exceptions import get_exception


class DBSqlite:
    def __init__(self, db_file_path: str, batch_size=100, echo=False):
        self.file = db_file_path
        self.batch_size = batch_size
        self.echo = echo

    def get_sqlite_engine(self):
        try:
            engine = create_engine(f"sqlite:///{self.file}", future=True, echo=self.echo).\
                execution_options(stream_results=self.echo,
                                  isolation_level="AUTOCOMMIT")

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
            sys.stderr.write(f"Unable to Create Database Connection: {get_exception(e)}")
            return None

    @staticmethod
    def get_db_session(engine):
        session = Session(bind=engine)
        return session


class DBPostgres:
    def __init__(self, **kwargs):
        self.username = kwargs["username"]
        self.password = kwargs["password"]
        self.host = kwargs["host"]
        self.port = kwargs["port"]
        self.db = kwargs["database"]

    def _set_engine(self):
        return create_async_engine(
            self.get_uri(),
            echo=False,
            future=True
        )

    def get_uri(self):
        credentials = {
            "drivername": "postgresql+asyncpg",
            "username": self.username,
            "password": self.password,
            "host": self.host,
            "port": self.port,
            "database": self.db
        }
        return sa.engine.URL.create(**credentials)

    def get_db_engine(self):
        return self._set_engine()

    @staticmethod
    def get_db_session(async_engine):
        async_session = async_sessionmaker(
            bind=async_engine,
            autoflush=True,
            expire_on_commit=False,
            future=True,
            class_=AsyncSession
        )
        return async_session()
