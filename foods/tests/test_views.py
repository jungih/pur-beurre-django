import unittest
import json
from unittest.mock import patch
from django.test import TestCase, Client
from foods.views import search, http_request, Scrap
from django.urls import reverse
from django.contrib.auth.models import User


class ViewsTest(TestCase):
    """Index view test"""

    def test_index_page(self):
        """Test status_code return"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


@patch('foods.views.requests.get')
class SearchViewTest(unittest.TestCase):
    """detail veiw function test3"""

    def test_status_code(self, mock_get):
        """ Test status_code return"""

        self.client = Client()
        mock_get.return_value.ok = False
        view_response = self.client.get(
            reverse('foods:search'), {'query': 'nutella'})
        self.assertEqual(view_response.status_code, 200)

    def test_request_error(self, mock_get):
        """Request Error Test"""

        mock_get.return_value.ok = False
        mock_get.return_value.status_code = 500
        response = http_request(None)
        self.assertEqual(response['status'], 'Error: 500')

    def test_request_whit_zero_response(self, mock_get):
        """0 porudcuts found"""

        mock_get.return_value.ok = True  # status = ok
        mock_get.return_value.json.return_value = {
            'count': 0}  # .json() mock
        response = http_request(None)
        self.assertEqual(response['status'], "Aucun produit n'a été trouvé.")

    def test_request_response(self, mock_get):
        """requset success"""

        mock_get.return_value.ok = True  # status = ok
        mock_get.return_value.json.return_value = {
            'count': 1,
            'products': [{'product_name_fr': 'Nutella'}]
        }  # .json() mock
        response = response = http_request(None)

        PROPERTIES = [
            'code',
            'product_name_fr',
            'brands',
            'quantity',
            'image_url',
            'image_small_url',
            'categories_hierarchy',
            'nutrition_grades'

        ]
        # check for keys in 'products' dictioinary in response
        for key in PROPERTIES:
            for product in response['products']:
                self.assertTrue(key in product)
        # Check value of 'status' in response
        self.assertEqual(response['status'], 'ok')


@patch('foods.views.requests.get')
class SubViewTest(unittest.TestCase):
    """Test Sub View3"""

    def setUp(self):
        self.client = Client()
        self.code = '00000'

        # Create a dummy session
        session = self.client.session
        data = {"products": [
            {"code": self.code, "categories_hierarchy": "None"}]}
        session['data'] = json.dumps(data)
        session.save()

    def test_status_code_200(self, mock_requests):
        """Check if page loads correctly"""

        # mock requests.get
        mock_requests.return_value.ok = True
        mock_requests.return_value.json.return_value = {'count': 0}
        response = self.client.get(reverse('foods:subs', args=[self.code]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['status'], "Aucun produit n'a été trouvé.")

    def test_status_code_404(self, mock_requests):
        """Check for error 404"""

        mock_requests.return_value.ok = True
        mock_requests.return_value.json.return_value = {'count': 0}
        response = self.client.get(reverse('foods:subs', args=["no_code"]))
        self.assertEqual(response.status_code, 404)


class DetailView(unittest.TestCase):

    @patch('foods.views.Scrap')
    def test_context(self, mock_scrap):
        """Test context values and status_code"""

        c = Client()
        mock_scrap.return_value.get_div.return_value = "div"
        mock_scrap.return_value.get_img.return_value = "img"
        mock_scrap.return_value.get_name.return_value = "name"

        response = c.get(reverse('foods:detail', args=['product_code']))

        self.assertEqual(response.context['score'], "div")
        self.assertEqual(response.context['nutrient'], "div")
        self.assertEqual(response.context['image_url'], "img")
        self.assertEqual(response.context['name'], "name")
        self.assertEqual(response.context['code'], "product_code")

        self.assertEqual(response.status_code, 200)


class PagesWithLogin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

    def test_email_update(self):
        """Test if account view redirects page after updating user's e-mail"""
        response = self.client.post(reverse('users:account'), {
                                    'email': 'abc@abc.com'})
        self.assertRedirects(response, reverse('users:account'))

    def test_save_post(self):
        """test a success post"""

        self.data = {
            "code": "1234567",
            "product_name_fr": "nutella",
            'image_small_url': "image.jpg",
            "nutrition_grades": "a",
            "brands": "ferrero",
            "quantity": "500g"
        }
        self.data = json.dumps(self.data)
        response = self.client.post(reverse('foods:save'), {
            "sub": self.data, "product": self.data})

        self.assertEqual(response.status_code, 201)

    def Test_myfoods_view(self):

        response = self.client.get(reverse('foods:myfoods'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['myfoods'])
