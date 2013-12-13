import unittest
from mock import patch, MagicMock

import flask_ssl_skeleton


class SkeletonTestCase(unittest.TestCase):
    testuser = 'unit'
    testpass = 'pass'

    def setUp(self):
        self.app = flask_ssl_skeleton.app
        self.app.secret_key = "Unit secret"
        self.client = self.app.test_client()

    def test_root_returns_form_when_not_logged_on(self):
        rv = self.client.get('/')
        self.assertTrue('<form method="POST">' in rv.data)

    def test_admin_redirects_to_login_when_not_logged_in(self):
        rv = self.client.get('/admin')
        self.assertEqual(302, rv.status_code)
        self.assertTrue(rv.headers['Location'].endswith('/'))

    #this isn't a great test...
    @patch('flask_ssl_skeleton.User', autospec=True)
    def test_root_redirects_when_logged_in(self, f):
        with self.app.test_request_context():
            rv = self.client.post('/', data=dict(username='admin', password='password'))
            self.assertEquals(302, rv.status_code)
            self.assertTrue(rv.headers['Location'].endswith('/admin'))
