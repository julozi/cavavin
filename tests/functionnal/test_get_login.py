# coding=utf-8

from cavavin.models import User
from tests import db
from tests import create_user
from tests.functionnal import CavavinTestCase
from urlparse import urlparse


class Exists(CavavinTestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_exists(self):
        """ GET /users/login exists """
        response = self.get('/users/login')
        self.assertNotIn(response.status_code, [404, 500])


class Redirect(CavavinTestCase):

    def setUp(self):
        db.create_all()
        create_user(id=1)
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_redirect_when_already_logged_in(self):
        """ GET /users/login redirect to homepage when user already logged in """
        response = self.get('/users/login', user=User.query.get(1))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, '/racks')
