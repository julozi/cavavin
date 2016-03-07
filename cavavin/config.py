# -*- coding: utf-8 -*-

__all__ = ['DefaultConfig']


class DefaultConfig(object):
    DEBUG = False
    TESTING = False

    # Generated using import os; os.urandom(24).encode('hex')
    # Must be specified
    SECRET_KEY = None

    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
