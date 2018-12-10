from . import *


class TestSearch(TestCase):
    """Test search view"""

    def create_product(self):
        return Food.objects.create(
            product_name='test'
        )

    def test_create_object(self):
        """ Test object created"""

        obj = self.create_product()
        self.assertTrue(isinstance(obj, Food))
        # __str__() returns product name
        self.assertEqual(str(obj), obj.product_name)
