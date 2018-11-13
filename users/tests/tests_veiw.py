from django.test import TestCase
from users.forms import EmailForm
from django.urls import reverse


class EmailFormTest(TestCase):
    def test_email_form_label(self):
        form = EmailForm()
        self.assertTrue(form.fields['email'].label == 'E-mail :')


class RegistrerView(TestCase):
    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_error(self):
        response = self.client.post(
            reverse('register'), {"username": "test", "passward": "test4321"})
        self.assertFormError(errors)
