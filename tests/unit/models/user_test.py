from tests.unit.unit_base_test import BaseTest
from models.user import UserModel


class UserTest(BaseTest):
    def test_create_user(self):
        user = UserModel('test', 'abcd')

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, 'abcd')
