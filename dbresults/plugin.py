import threading
import os
import dbresults.models
import pytest

from datetime import datetime


@pytest.fixture(scope="session")
def dbresults_custom():
    """ Used as a way to send custom text to the results database from within
    the test code. Whatever you place in its dict will be saved in a TEXT
    column.
    """
    return {}


class ResultsToDB(object):
    def __init__(self, alch_url):
        self.sql_eng = dbresults.models.init_engine_from(alch_url)
        self.sql_sess = dbresults.models.init_session(self.sql_eng)

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            self.tr = dbresults.models.RunResult(
                name=report.nodeid,
                status=report.passed, session=self.test_sess,
                outcome=report.outcome, duration=report.duration)

    def pytest_runtest_makereport(self, item, call):
        if call.when == "teardown":
            custom = item.funcargs.get("dbresults_custom", {})
            self.tr.custom = "{}".format(custom)
            self.sql_sess.add(self.tr)

    def pytest_sessionstart(self, session):
        self.test_sess = dbresults.models.TestSession(
            date=datetime.now(),
            name="pid_thid:{}_{}".format(
                os.getpid(), threading.current_thread().ident))
        self.sql_sess.add(self.test_sess)

    def pytest_sessionfinish(self, session):
        self.sql_sess.commit()


def pytest_unconfigure(config):
    res2db = getattr(config, "_res2db", None)
    if res2db:
        config.pluginmanager.unregister(res2db)


def pytest_configure(config):
    if config.option.sqlalch_url and not _is_running_on_slave(config):
        config._res2db = ResultsToDB(config.option.sqlalch_url)
        config.pluginmanager.register(config._res2db)


def pytest_addoption(parser):
    group = parser.getgroup(
        "dbresults",
        "store results in a db with support for distributed testing")
    group.addoption("--dbresults", action="store", dest="sqlalch_url",
                    default=None,
                    help="enable saving of results into a database.")


def _is_running_on_slave(config):
    return hasattr(config, 'slaveinput')


def _debug(msg):
    ps_info = "{}_{}".format(os.getpid(), threading.current_thread().ident)
    file_name = "dbg.log".format(ps_info)
    with open(file_name, "a+") as dbg_log:
        dbg_log.write("{}: {}\n".format(ps_info, msg))


