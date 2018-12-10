from django.test import TestCase
from users.forms import EmailForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse


class UsersView(TestCase):

    def test_email_form_label(self):

        form = EmailForm()
        self.assertTrue(form.fields['email'].label == 'E-mail :')

    def test_register_page_load(self):

        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_new_user(self):

        new_username = 'testuser11'
        data = {"username": new_username,
                "password1": "testing4321",
                "password2": "testing4321"}
        self.client.post(reverse('register'), data, follow=True)
        new_user = User.objects.get(username=new_username)
        self.assertEqual(new_user.username, new_username)


class EamilUpdate(TestCase):

    def setUp(self):

        # Create user
        self.user = User.objects.create_user(
            username='testuser', password='testing4321')
        # login is required for account page
        self.client.login(
            username='testuser', password='testing4321')

    def test_account_page_load(self):

        response = self.client.get(reverse('users:account'))
        self.assertEqual(response.status_code, 200)

    def test_post_email_update(self):
        """Test email update"""

        new_email = 'abc@abc.com'

        self.client.post(reverse('users:account'), {'email': new_email})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, new_email)
