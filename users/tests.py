from django.test import TestCase
from users.forms import EmailForm


class EmailFormTest(TestCase):
    def test_email_form_label(self):
        form = EmailForm()
        self.assertTrue(form.fields['email'].label == 'E-mail :')
