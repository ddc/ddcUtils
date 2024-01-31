# -*- encoding: utf-8 -*-
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


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
