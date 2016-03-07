# coding=utf-8

from flask import Flask
import logging.config

from .config import DefaultConfig
from .extensions import db


def create_app(config=None):
    """Create a Flask app
    Using application factory like describe here :
    http://flask.pocoo.org/docs/0.10/patterns/appfactories/#app-factories
    """

    app = Flask(__name__)

    configure_app(app, config)
    configure_logging(app)
    configure_extensions(app)
    configure_crash_handler(app)

    register_blueprints(app)

    return app


def configure_extensions(app):
    """Configure extensions defined in mouse.extensions.py"""
    app.logger.info('configuring extensions')

    # flask-sqlalchemy
    db.app = app
    db.init_app(app)

    # Enable Foreign key constraint when using Sqlite
    if db.engine.name == 'sqlite':  # pragma: no cover
        from .extensions import sqlite_foreign_key_event, remove_warning_decimal_for_sqlite

        sqlite_foreign_key_event(app)
        remove_warning_decimal_for_sqlite(app)


def configure_app(app, config=None):
    """Load configuration

    The default configuration is overwritten by `config` or custom config
    located in app.cfg

    """
    app.logger.debug('Configuring application')

    app.config.from_object(DefaultConfig)

    if not config:  # pragma: no cover
        app.logger.debug('Load config from app.cfg')
        app.config.from_pyfile('../app.cfg', silent=True)
    else:
        app.logger.debug('Load config from %s' % config)
        app.config.from_pyfile(config)


def register_blueprints(app):
    """Register blueprints
    """
    app.logger.debug('Registering blueprints')

    from .controllers import register_all_blueprints
    register_all_blueprints(app)


def configure_crash_handler(app):  # pragma: no cover
    """Add handler for logging application severe errors, such as HTTP:500, uncatch Exception"""
    if not app.debug and not app.testing:
        app.logger.info('configuring crash handler')

        from werkzeug.exceptions import HTTPException
        import sys
        import traceback

        def error_handler(error):
            from flask import request

            if isinstance(error, HTTPException):
                description = error.get_description(request.environ)
                code = error.code
                name = error.name
            else:
                description = "Traceback de l'appel:\n\t---\n"
                (type_except, value, tb) = sys.exc_info()
                trace = "\t".join(traceback.format_exception(type_except, value, tb))
                description += trace
                code = 500
                name = 'Internal Server Error'

            msg = "Code:%s\n\tName:%s\n\tMessage:%s\n" % (code, name, description)
            app.logger.error(msg)
            return description, code

        # Catch error 500
        app.register_error_handler(500, error_handler)
        # Catch all Exception
        app.register_error_handler(Exception, error_handler)

        def log_uncaught_exceptions(ex_cls, ex, tb):
            app.logger.critical(''.join(traceback.format_tb(tb)))
            app.logger.critical('{0}: {1}'.format(ex_cls, ex))

        sys.excepthook = log_uncaught_exceptions


def overwrite_dict(src, ovw):
    """Overwrite a dict with another one.
    Existing keys will be overwritten. New keys are added
    """

    import collections
    for k, v in ovw.iteritems():
        if isinstance(v, collections.Mapping):
            r = overwrite_dict(src.get(k, {}), v)
            src[k] = r
        else:
            src[k] = ovw[k]
    return src


def configure_logging(app):  # pragma: no cover
    """Configure logging"""
    if app.testing:
        # Skip test mode. Just check standard output.
        return

    if 'LOGGING' in app.config:
        app.logger  # Needed to configure the Flask logger, so we can modify it after
        config_dict = app.config['LOGGING']

        if 'LOGGING_EXT' in app.config:
            config_dict = overwrite_dict(config_dict, app.config['LOGGING_EXT'])

        logging.config.dictConfig(config_dict)
