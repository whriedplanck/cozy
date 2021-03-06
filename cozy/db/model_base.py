import logging
import os

from peewee import Model
from playhouse.sqliteq import SqliteQueueDatabase

from cozy.control.application_directories import get_data_dir

log = logging.getLogger("db")

_db = None


def get_sqlite_database():
    global _db
    return _db


def database_file_exists():
    return os.path.exists(os.path.join(get_data_dir(), "cozy.db"))


def __open_database():
    global _db
    if not os.path.exists(get_data_dir()):
        os.makedirs(get_data_dir())
    _db = SqliteQueueDatabase(os.path.join(get_data_dir(), "cozy.db"), queue_max_size=128, results_timeout=15.0,
                              timeout=15.0, pragmas=[('cache_size', -1024 * 32), ('journal_mode', 'wal')])


__open_database()


class ModelBase(Model):
    class Meta:
        database = _db
