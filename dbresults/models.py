import sys
import os

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.engine.url

from sqlalchemy import (Column, Integer, String, Boolean, DateTime, ForeignKey,
                        Float)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# ENGINE_URI = os.environ.get(
#     "bamboo_SQLALCHEMY_URI", "mysql://root@localhost/alchemy")

# engine = sqlalchemy.create_engine(ENGINE_URI)
# session_cls = sqlalchemy.orm.sessionmaker(engine)
# session = session_cls()


def init_engine_from(url):
    engine = sqlalchemy.create_engine(url)
    return engine


def init_engine(driver="mysql", user="root", pwd="", host="localhost",
                port=3306, db="alchemy", query=None):
    url = sqlalchemy.engine.url.URL(driver, user, pwd, host, port, db, query)
    engine = sqlalchemy.create_engine(url)
    return engine


def init_session(engine):
    session_cls = sqlalchemy.orm.sessionmaker(engine)
    return session_cls()


class TestSession(Base):
    __tablename__ = "test_sessions"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    name = Column(String(250))


class RunResult(Base):
    __tablename__ = "test_case_results"

    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    message = Column(String(500))
    status = Column(Boolean)
    session_id = Column(Integer, ForeignKey("test_sessions.id"))
    duration = Column(Float)

    session = relationship("TestSession")


def sync():
    print "sync-ing"
    Base.metadata.create_all(init_engine())


def drop():
    print "drop-ing"
    Base.metadata.drop_all(init_engine())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        pass
    elif sys.argv[1] == "drop":
        drop()
    elif sys.argv[1] == "sync":
        sync()
    else:
        print "Tell me what you want"
