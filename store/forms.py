from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label=("Enter Password:"), widget=forms.PasswordInput(attrs={'placeholder':'Enter 8 Digit Alphanumeric Password'}))
    password2 = forms.CharField(label=("Confirm Password:"), widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}), help_text="Enter the same password as before, for verification.")
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username':None,
            'email':None,
        }
        labels = {
            'username': 'Username:',
            'email':'Email:'
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder':'Enter Username'}),
            'email': forms.EmailInput(attrs={'placeholder':'user@email.com'}),
        }