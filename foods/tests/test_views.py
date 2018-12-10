from . import *
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from unittest.mock import patch


class TestIndex(TestCase):
    """Index view test"""

    def test_index_page(self):
        """Test status code"""

        # URL from project directory
        response = self.client.get(reverse('index'))
        # URL from foods app directory
        foods_response = self.client.get(reverse('foods:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(foods_response.status_code, 200)


class TestQueries(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='12345')

        cls.product_1 = Food.objects.create(
            code='0001',
            product_name='product_1',
            nutrition_grade_fr='c',
            categories_fr='leve_1,level_2')
        cls.product_2 = Food.objects.create(
            code='0002',
            product_name='product_2',
            nutrition_grade_fr='a',
            categories_fr='leve_1')

    def setUp(self):
        # setup relationships
        selected = self.product_1
        selected.author.add(self.user)
        selected.substitute.add(self.product_2)
        selected.save()
        self.client.login(username='test', password='12345')

    def test_search(self):
        """Test Search View"""

        search_query = 'product'
        # Implement variable "query" in URL
        response = self.client.get(
            reverse('foods:search'), {'query': search_query})

        # Test if search results 'product' in its name
        for product in response.context['products']:
            self.assertTrue(search_query in product.product_name)
        self.assertEqual(response.context['query'], search_query)
        self.assertEqual(response.context['status'], 'ok')

    def test_searh_zero_result_found(self):
        """Search View returns zeor results"""

        search_query = 'test'
        # Implement variable "query" in URL
        response = self.client.get(
            reverse('foods:search'), {'query': search_query})
        # check status message
        self.assertEqual(
            response.context['status'], "Aucun produit n'a été trouvé.")

    def test_sub_view(self):
        """Sub View"""
        selected_product = self.product_1
        response = self.client.get(
            reverse('foods:subs', args=[selected_product.code]))

        # Test if selected product parsed correctly in the context
        self.assertEqual(response.context['selected'], selected_product)

    def test_sub_zero_result_found(self):
        selected_product = self.product_2

        response = self.client.get(
            reverse('foods:subs', args=[selected_product.code]))
        self.assertEqual(
            response.context['status'], "Aucun produit n'a été trouvé.")

    def test_detail_veiw(self):
        selected_product = self.product_1

        response = self.client.get(
            reverse('foods:detail', args=[selected_product.code]))
        self.assertEqual(
            response.context['product'], selected_product)
        self.assertEqual(
            response.context['image_score'],
            f'foods/img/nutriscore-{selected_product.nutrition_grade_fr}.svg')

    def test_mentions_view(self):
        """Test Mentions View"""
        response = self.client.get(reverse('foods:mentions'))
        self.assertEqual(response.status_code, 200)

    def test_save_product_already_saved(self):

        # Selecting same products already saved
        selected = self.product_1
        sub = self.product_2

        response = self.client.post(reverse('foods:save'), {
            "sub": sub.id, "selected": selected.id})

        self.assertEqual(response.status_code, 201)

    def test_save_new_substitute(self):

        # Creating new product
        product_3 = Food.objects.create(
            code='0003',
            product_name='product_2',
            nutrition_grade_fr='b',
            categories_fr='leve_1,level2,level,3')

        # Selecting new product as a substitute
        selected = self.product_2
        sub = product_3

        response = self.client.post(reverse('foods:save'), {
            "sub": sub.id, "selected": selected.id})
        self.assertEqual(response.status_code, 201)

    def test_myfoods_view(self):
        """myfoods View"""

        self.client.login(username='test', password='12345')
        response = self.client.get(reverse('foods:myfoods'))
        self.assertTrue(response.context['myfoods'])

    def test_delete_view_remove_orignal_product(self):
        """Deleting original product"""

        original = self.product_1

        response = self.client.get(
            reverse('foods:delete_selected', args=[original.id]))
        self.assertEqual(response.context['selected'], self.product_1)
        self.assertFalse(response.context['sub'])

        remove = self.client.post(
            reverse('foods:delete_selected', args=[original.id]))
        # Page redirects after the removal
        self.assertEqual(remove.status_code, 302)

    def test_delete_view_remove_substitute(self):
        """Deleting substitute product"""

        original = self.product_1
        sub = self.product_2
        response = self.client.get(
            reverse('foods:delete_sub', args=[original.id, sub.id]))
        self.assertEqual(response.context['selected'], self.product_1)
        self.assertEqual(response.context['sub'], self.product_2)

        remove = self.client.post(
            reverse('foods:delete_sub', args=[original.id, sub.id]))
        # Page redirects after the removal
        self.assertEqual(remove.status_code, 302)
