from models.user import UserModel
from flask.testing import FlaskClient
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app as client:
            with self.app_context():
                request = client.post('/register', data={'username': 'malavolta', 'password': '234'})

                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('malavolta'))
                self.assertDictEqual(d1={'message': 'user created successfully.'},
                                     d2=json.loads(request.data))

    def test_register_and_login(self):
        with self.app as c:
            with self.app_context():
                c.post('/register', data={'username': 'malavolta', 'password': '234'})
                auth_request = c.post('/auth',
                                      data=json.dumps({'username': 'malavolta', 'password': '234'}),
                                      headers={'Content-Type': 'application/json'}
                                      )

                self.assertIn('access_token', json.loads(auth_request.data).keys())

    def test_register_duplicate_user(self):
        with self.app as c:
            with self.app_context():
                c.post('/register', data={'username': 'malavolta', 'password': '234'})
                response = c.post('/register', data={'username': 'malavolta', 'password': '234'})

        self.assertEquals(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {'message': 'username is already exist'})
