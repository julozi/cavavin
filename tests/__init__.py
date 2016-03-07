# coding=utf-8

import hashlib

from cavavin.app import create_app
from cavavin.extensions import db

# Initialize Flask application for testing
app = create_app(config='../testing.cfg')
test_client = app.test_client()

app.logger.debug('db URI : %s', app.config.get('SQLALCHEMY_DATABASE_URI', 'rien'))
from cavavin.models import *  # noqa : to register all Model


def create_user(id, email=None, password=None, lastname=None, firstname=None):

    user = User(id=id,
                email=email if email is not None else u'%s@macavavin.fr' % id,
                password=unicode(hashlib.md5(password if password is not None else u'secret').hexdigest()),
                lastname=lastname if lastname is not None else u'Lastname%s' % id,
                firstname=firstname if firstname is not None else u'Firstname%s' % id)
    db.session.add(user)
    return user
