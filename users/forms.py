from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'data-rule-required': 'true',
            'data-rule-minlength': '5'
        })
    )

    password = forms.CharField(min_length=5, max_length=10,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'data-rule-passwd': 'true'
        }),
        label="Password"

    )



class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'data-rule-email': 'true'
        })
    )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'data-rule-required': 'true',
            'data-rule-minlength': '5'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'data-rule-passwd': 'true'
        }),
        label="Password"

    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'data-rule-passwd': 'true'
        }),
        label="Confirm Password"  
    )
