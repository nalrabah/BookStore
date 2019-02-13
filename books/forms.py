from django import forms
from django.contrib.auth.models import User
from .models import Book

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class SigninForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

        