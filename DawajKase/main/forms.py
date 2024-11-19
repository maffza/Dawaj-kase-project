from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(max_length=64)
    password = forms.PasswordInput(max_length=256)