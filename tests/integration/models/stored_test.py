from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoredTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all(), [], "")

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'))

    def test_store_relations(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 20.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertIsNotNone(store.items.count(), 1)
            self.assertEquals(store.items.first().name, 'test_item')

    def test_store_json(self):
        store = StoreModel('test')
        expected = {
            'name': 'test',
            'items': []
        }

        self.assertDictEqual(store.json(), expected)

    def test_store_items_json(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 20.99, 1)

            store.save_to_db()
            item.save_to_db()
            expected = {
                'name': 'test',
                'items': [{'name': 'test_item', 'price': 20.99}]
            }

            self.assertDictEqual(store.json(), expected)

