from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app as c:
            with self.app_context():
                response = c.post('store/test')

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual(json.loads(response.data), {'name': 'test', 'items': []})

    def test_create_duplicate_store(self):
        with self.app as c:
            with self.app_context():
                c.post('store/test')
                response = c.post('store/test')

                self.assertEqual(response.status_code, 400)
                self.assertEqual(json.loads(response.data),
                                 {'message': "A store with name 'test' already exists."})

    def test_delete_store(self):
        with self.app as c:
            with self.app_context():
                store = StoreModel('test').save_to_db()
                resp = c.delete('/store/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Store deleted'})

    def test_find_store(self):
        with self.app as c:
            with self.app_context():
                store = StoreModel('test').save_to_db()
                resp = c.get('store/test')

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(json.loads(resp.data), {'name': 'test', 'items': []})

    def test_store_not_found(self):
        with self.app as c:
            with self.app_context():
                response = c.get('/store/test')

                self.assertEqual(response.status_code, 404)
                self.assertEqual(json.loads(response.data), {'message': 'Store not found'})

    def test_store_find_with_items(self):
        with self.app as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_iten', 19.99, 1).save_to_db()

                response = c.get('/store/test')

                self.assertEqual(response.status_code, 200)
                self.assertEqual(json.loads(response.data), {'items': [{'name': 'test_iten', 'price': 19.99}], 'name': 'test'})

    def test_store_list(self):
        with self.app as c:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = c.get('/stores')

                self.assertEqual(resp.status_code, 200)
                self.assertEqual({'stores': [{'items': [], 'name': 'test'}]}, json.loads(resp.data))

    def test_store_list_with_items(self):
        with self.app as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_iten', 19.99, 1).save_to_db()

                response = c.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertEqual(json.loads(response.data), {'stores': [{'items': [{'name': 'test_iten', 'price': 19.99}], 'name': 'test'}]})