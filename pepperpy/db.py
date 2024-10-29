# pypepper/db.py


def connect_db(db_path=":memory:"):
    import sqlite3

    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    return conn
