from time import sleep
from typing import List

from pymongo import MongoClient
from sqlalchemy import Column, Integer, String, create_engine, select, update, insert
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import OperationalError

from counter.domain.models import ObjectCount
from counter.domain.ports import ObjectCountRepo


class CountInMemoryRepo(ObjectCountRepo):

    def __init__(self):
        self.store = dict()

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        if object_classes is None:
            return list(self.store.values())

        return [self.store.get(object_class) for object_class in object_classes]

    def update_values(self, new_values: List[ObjectCount]):
        for new_object_count in new_values:
            key = new_object_count.object_class
            try:
                stored_object_count = self.store[key]
                self.store[key] = ObjectCount(key, stored_object_count.count + new_object_count.count)
            except KeyError:
                self.store[key] = ObjectCount(key, new_object_count.count)


class CountMongoDBRepo(ObjectCountRepo):

    def __init__(self, host, port, database):
        self.__host = host
        self.__port = port
        self.__database = database

    def __get_counter_col(self):
        client = MongoClient(self.__host, self.__port)
        db = client[self.__database]
        counter_col = db.counter
        return counter_col

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        counter_col = self.__get_counter_col()
        query = {"object_class": {"$in": object_classes}} if object_classes else None
        counters = counter_col.find(query)
        object_counts = []
        for counter in counters:
            object_counts.append(ObjectCount(counter['object_class'], counter['count']))
        return object_counts

    def update_values(self, new_values: List[ObjectCount]):
        counter_col = self.__get_counter_col()
        for value in new_values:
            counter_col.update_one({'object_class': value.object_class}, {'$inc': {'count': value.count}}, upsert=True)


class CountPostgresDBRepo(ObjectCountRepo):
    Base = declarative_base()

    class DbObjectCount(Base):
        __tablename__ = "object_count"
        id = Column(Integer, primary_key=True, autoincrement=True)
        object_class = Column(String(30), unique=True, nullable=False)
        count = Column(Integer, unique=False, nullable=False)

    def __init__(self, host, port, database, user, password):
        attempts = 0
        while True:
            attempts += 1
            try:
                self.__engine = create_engine(
                    f"postgresql://{user}:{password}@{host}:{port}/{database}",
                    echo=True,
                    future=True,
                    pool_timeout=30,
                )
                self.Base.metadata.create_all(self.__engine)
                break
            except OperationalError:
                if attempts > 3:
                    raise ConnectionError("Cannot connect to postgres instance.")
                sleep(5)

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        session = Session(self.__engine)

        stmt = select(self.DbObjectCount).where(
            self.DbObjectCount.object_class.in_(object_classes) if object_classes else True
        )
        object_counts = []
        for counter in session.scalars(stmt):
            object_counts.append(ObjectCount(counter.object_class, counter.count))
        return object_counts

    def update_values(self, new_values: List[ObjectCount]):
        with Session(self.__engine) as session:
            for value in new_values:
                stmt = select(self.DbObjectCount).where(self.DbObjectCount.object_class == value.object_class)
                if session.scalar(stmt):
                    stmt = update(self.DbObjectCount).where(self.DbObjectCount.object_class == value.object_class).values(count=self.DbObjectCount.count + value.count)
                else:
                    stmt = insert(self.DbObjectCount).values(object_class=value.object_class, count=value.count)
                session.execute(stmt)
            session.commit()
