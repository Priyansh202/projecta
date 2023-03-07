from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
 
    password = forms.CharField(label='Password', widget=forms.PasswordInput)