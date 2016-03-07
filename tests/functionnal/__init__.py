# coding=utf-8

from pyquery import PyQuery
from tests import app
from unittest import TestCase


class CavavinTestCase(TestCase):

    def get(self, *args, **kwargs):
        with app.test_client() as c:
            if 'user' in kwargs:
                user = kwargs.pop('user')
                with c.session_transaction() as session:
                    session['user'] = user.to_dict()

            return c.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        with app.test_client() as c:
            if 'user' in kwargs:
                user = kwargs.pop('user')
                with c.session_transaction() as session:
                    session['user'] = user.to_dict()

            return c.post(*args, **kwargs)

    def assertHasFlashMessage(self, data, message):
        d = PyQuery(data)
        self.assertIn(message, d("div.alert").text())
