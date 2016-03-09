# coding=utf-8

import flask

from tests import app, db
from tests import create_user
from tests.functionnal import CavavinTestCase
from urlparse import urlparse


class Exists(CavavinTestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_exists(self):
        """ POST /users/login exists """
        response = self.post('/users/login')
        self.assertNotIn(response.status_code, [404, 500])


class Login(CavavinTestCase):

    def setUp(self):
        db.create_all()
        create_user(id=1,
                    email=u'test@macavavin.fr',
                    password=u'test',
                    firstname=u'John',
                    lastname=u'Doe')
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_login(self):
        """ POST /users/login with valid credential """
        with app.test_client() as client:
            data = {
                u'email': u'test@macavavin.fr',
                u'password': u'test'
            }
            response = client.post('/users/login', data=data)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(urlparse(response.location).path, '/racks')
            self.assertIn(u'user', flask.session)
            self.assertDictEqual(flask.session[u'user'],
                                 {u'id': 1,
                                  u'email': u'test@macavavin.fr',
                                  u'firstname': u'John',
                                  u'lastname': u'Doe'})

    def test_login_when_already_logged_in(self):
        """ POST /users/login with valid credential when already logged in """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user'] = {u'id': 12,
                                   u'email': u'other@cavavin.fr',
                                   u'firstname': u'Other',
                                   u'lastname': u'User'}
            data = {
                u'email': u'test@macavavin.fr',
                u'password': u'test'
            }
            response = client.post('/users/login', data=data)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(urlparse(response.location).path, '/racks')
            self.assertIn(u'user', flask.session)
            self.assertDictEqual(flask.session[u'user'],
                                 {u'id': 1,
                                  u'email': u'test@macavavin.fr',
                                  u'firstname': u'John',
                                  u'lastname': u'Doe'})
