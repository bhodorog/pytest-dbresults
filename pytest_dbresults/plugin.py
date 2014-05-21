import threading
import os
import os.path

from datetime import datetime
import dbresults.models

test_sess = None
sql_sess = None


def pytest_runtest_logreport(report):
    if report.when == "call" and sql_sess and test_sess:
        tr = dbresults.models.RunResult(
            name=report.nodeid, message="bubu",
            status=report.passed, session=test_sess, duration=report.duration)
        sql_sess.add(tr)


def pytest_unconfigure(config):
    _delete_touches()
    if sql_sess:
        sql_sess.commit()


def pytest_configure(config):
    """when xdist is installed and used from cmd line (e.g. with -n arg) this
    hook is called 3 times, once for master ps, and again from each slave
    ps. To avoid this when xdist is installed and used from cmd line don't init
    db here, let the other xdist hook to do it"""
    if not _is_touched():
        _touch("configure")
        _init_db()


def _init_db():
    global test_sess, sql_sess
    test_sess = dbresults.models.TestSession(
        date=datetime.now(),
        name="pid_thid:{}_{}".format(
            os.getpid(), threading.current_thread().ident))
    sql_sess = dbresults.models.session_cls()
    sql_sess.add(test_sess)


ID_DB_FILENAME = "id.tmp"


def _delete_touches():
    if os.path.exists(ID_DB_FILENAME):
        os.remove(ID_DB_FILENAME)


def _touch(id_msg):
    with open(ID_DB_FILENAME, "w") as idfile:
        idfile.write("{}\n".format(id_msg))


def _is_touched():
    if not os.path.exists(ID_DB_FILENAME):
        return None
    with open(ID_DB_FILENAME) as idfile:
        return idfile.readline()


def _debug(msg):
    ps_info = "{}_{}".format(os.getpid(), threading.current_thread().ident)
    file_name = "dbg.log".format(ps_info)
    with open(file_name, "a+") as dbg_log:
        dbg_log.write("{}: {}\n".format(ps_info, msg))


