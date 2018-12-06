import unittest
import json
from unittest.mock import patch
from django.test import TestCase, Client
from foods.views import search, Scrap
from django.urls import reverse
from django.contrib.auth.models import User


class TestIndex(TestCase):
    """Index view test"""

    def test_index_page(self):
        """Test status_code return"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


# @patch('foods.views.requests.get')
# class TestDetailView(unittest.TestCase):
#     def test_context(self, mock_requests):
#         """Test context values and status_code"""

#         c = Client()
#         mock_requests.return_value.text = "Hello world"

#         response = c.get(reverse('foods:detail', args=['product_code']))

#         self.assertEqual(
#             response.context['score'], 'Les données non présentes')
#         self.assertEqual(
#             response.context['nutrient'], 'Les données non présentes')
#         self.assertFalse(response.context['image_url'])
#         self.assertFalse(response.context['name'])
#         self.assertEqual(response.context['code'], "product_code")

#         self.assertEqual(response.status_code, 200)


# class TestLogin(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='test', password='12345')
#         self.client.login(username='test', password='12345')

#     def test_save_post(self):
#         """test a success post"""

#         self.data = {
#             "code": "1234567",
#             "product_name_fr": "nutella",
#             'image_small_url': "image.jpg",
#             "nutrition_grades": "a",
#             "brands": "ferrero",
#             "quantity": "500g"
#         }
#         self.data = json.dumps(self.data)
#         response = self.client.post(reverse('foods:save'), {
#             "sub": self.data, "product": self.data})

#         self.assertEqual(response.status_code, 201)

#     def test_myfoods_view(self):

#         response = self.client.get(reverse('foods:myfoods'))
#         self.assertEqual(response.status_code, 200)
#         self.assertFalse(response.context['myfoods'])
