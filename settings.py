import os


def _database_path():
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, "logvmtraffic.db")
    return path

DATABASE_PATH = _database_path()
