from django import forms
from .models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=6, max_length=50)
    email = forms.EmailField()
    password = forms.CharField(min_length=8, max_length=32)
    password_repeat = forms.CharField(min_length=8, max_length=32)
    phone_number = forms.IntegerField(min_value=100000000, max_value=999999999999)
    number_prefix = forms.IntegerField(min_value=1, max_value=99)


class LoginForm(forms.Form):
    email = forms.EmailField(min_length=6, max_length=50)
    password = forms.CharField(min_length=8, max_length=32)

    def login(self, request):
        return User.objects.all().filter(
                email=self.cleaned_data.get('email'),
                password=self.cleaned_data.get('password')
            )
