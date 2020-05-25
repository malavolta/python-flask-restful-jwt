from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest


class StroredTest(UnitBaseTest):
    def test_create_stored(self):
        store = StoreModel('test')

        self.assertEquals(store.name,'test')