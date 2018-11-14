from django.test import TestCase
from users.forms import EmailForm
from django.contrib.auth.models import User
from django.urls import reverse


class TestEmailForm(TestCase):

    def test_email_form_label(self):
        form = EmailForm()
        self.assertTrue(form.fields['email'].label == 'E-mail :')


class TestRegistrerView(TestCase):

    def test_register(self):
        data = {"username": "testuser11",
                "password1": "testing4321",
                "password2": "testing4321"}
        response = self.client.post(reverse('register'), data, follow=True)
        self.assertEqual(response.status_code, 200)


class TestAccountView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

    def test_email_update(self):
        """Test if account view redirects page after updating user's e-mail"""
        response = self.client.post(reverse('users:account'), {
                                    'email': 'abc@abc.com'})
        self.assertRedirects(response, reverse('users:account'))
