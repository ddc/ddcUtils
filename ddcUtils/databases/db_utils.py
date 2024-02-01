# -*- encoding: utf-8 -*-
from ..exceptions import (
    DBAddException,
    DBExecuteException,
    DBFetchAllException,
    DBFetchValueException
)


class DBUtils:
    def __init__(self, session):
        self.session = session

    def add(self, stmt):
        try:
            self.session.add(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBAddException(e)
        else:
            self.session.commit()

    def execute(self, stmt):
        try:
            self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBExecuteException(e)
        else:
            self.session.commit()

    def fetchall(self, stmt):
        cursor = None
        try:
            cursor = self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBFetchAllException(e)
        else:
            self.session.commit()
            return cursor.mappings().all()
        finally:
            cursor.close() if cursor is not None else None

    def fetchone(self, stmt):
        cursor = None
        try:
            cursor = self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBFetchAllException(e)
        else:
            self.session.commit()
            return cursor.mappings().first()
        finally:
            cursor.close() if cursor is not None else None

    def fetch_value(self, stmt):
        cursor = None
        try:
            cursor = self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBFetchValueException(e)
        else:
            self.session.commit()
            return cursor.first()[0]
        finally:
            cursor.close() if cursor is not None else None


class DBUtilsAsync:
    def __init__(self, session):
        self.session = session

    async def add(self, stmt):
        try:
            self.session.add(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBAddException(e)
        else:
            await self.session.commit()

    async def execute(self, stmt):
        try:
            await self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBExecuteException(e)
        else:
            await self.session.commit()

    async def fetchall(self, stmt):
        cursor = None
        try:
            cursor = await self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBFetchAllException(e)
        else:
            await self.session.commit()
            return cursor.mappings().all()
        finally:
            cursor.close() if cursor is not None else None

    async def fetchone(self, stmt):
        cursor = None
        try:
            cursor = await self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBFetchAllException(e)
        else:
            await self.session.commit()
            return cursor.mappings().first()
        finally:
            cursor.close() if cursor is not None else None

    async def fetch_value(self, stmt):
        cursor = None
        try:
            cursor = await self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBFetchValueException(e)
        else:
            await self.session.commit()
            return cursor.first()[0]
        finally:
            cursor.close() if cursor is not None else None
