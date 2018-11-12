import unittest
from foods.views import search, http_request
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from foods.models import Foods


class ViewsTest(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class SearchViewTest(unittest.TestCase):
    def test_search_view(self):
        response = http_request({
            'search_simple': 1,
            'action': 'process',
            'nutriment_0': 'nutrition-score-fr',
            'nutriment_compare_0': 'lt',
            'nutriment_value_0': 11,
            'json': 1
        })
        self.assertTrue(response['status'] == 'o')