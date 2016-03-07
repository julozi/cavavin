# coding=utf-8
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def sqlite_foreign_key_event(app):
    """ Sets up an event listener for SQLite to try to have it run like a normal DBMS """
    from sqlalchemy import event

    app.logger.warning('Setting PRAGMA for foreign keys with Sqlite')

    def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute('pragma foreign_keys=ON')
        # dbapi_con.execute('PRAGMA case_sensitive_like=ON')

    event.listen(db.engine, 'connect', _fk_pragma_on_connect)


def remove_warning_decimal_for_sqlite(app):
    """ Removes Warning from SQLAlchemy when using Decimal type with SQlite database """
    from sqlalchemy.exc import SAWarning
    import warnings

    warnings.filterwarnings(action='ignore', category=SAWarning,
                            message='Dialect sqlite\+pysqlite does \*not\* support Decimal objects natively.​*\s.*​')
