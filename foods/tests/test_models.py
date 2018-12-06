from . import *
from foods.models import Food


class TestSearch(TestCase):
    """Test search view"""

    def create_article(self):
        return Food.objects.create(
            product_name='test'
        )

    def test_create_object(self):
        """ Test object created"""

        obj = self.create_article()
        self.assertTrue(isinstance(obj, Food))
        self.assertEqual(str(obj), obj.product_name)
        self.assertEqual(str(obj._meta.ordering[0]), 'pk')
