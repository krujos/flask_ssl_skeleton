import unittest
import flask_ssl_skeleton


class SkeletonTestCase(unittest.TestCase):

    def setUp(self):
        self.app = flask_ssl_skeleton.app
        self.app.secret_key = "Unit secret"
        self.client = self.app.test_client()

    def test_root_returns_form_when_not_logged_on(self):
        rv = self.client.get('/')
        self.assertTrue('<form method="POST">' in rv.data)

    def test_admin_returns_unauthorized_when_not_logged_in(self):
        rv = self.client.get('/admin')
        self.assertEqual(401, rv.status_code)

    def test_root_redirects_when_logged_in(self):
        rv = self.client.post('/', data=dict(username='admin', password='password'))
        self.assertEquals(302, rv.status_code)
        self.assertTrue(rv.headers['Location'].endswith('/admin'))
