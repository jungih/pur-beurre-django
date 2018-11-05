from django.forms import ModelForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton, InlineField, FormActions
from crispy_forms.layout import Layout, Div


class EmailForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.form_action = 'users:account'
        # self.helper.label_class = ''
        self.helper.field_class = 'mx-2'
        self.helper.layout = Layout(

            'email',
            StrictButton(
                'Enregistrer', css_class="btn-primary", type='submit'),

        )
        # self.helper.field_template = 'bootstrap3/layout/inline_field.html'

    class Meta:
        model = User
        fields = ['email', ]
        labels = {"email": "E-mail :"}
