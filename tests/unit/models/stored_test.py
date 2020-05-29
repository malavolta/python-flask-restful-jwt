from models.store import StoreModel
from tests.unit.unit_base_test import BaseTest


class StroredTest(BaseTest):
    def test_create_stored(self):
        store = StoreModel('test')

        self.assertEqual(store.name, 'test')
