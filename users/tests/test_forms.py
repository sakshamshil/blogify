from django.test import TestCase
from django.contrib.auth.models import User
from users.forms import LoginForm, SignupForm

class TestForms(TestCase):

    def setUp(self):
        self.valid_data_login = {
            'username': 'testuser',
            'password': 'Check123#'
        }

        self.invalid_data_login = {
            'username': 'eh',
            'password': 'eh'
        }

        self.valid_data_signup = {
            'email': 'testuser@gmail.com.com',
            'username': 'tstuser',
            'password1': 'Check123#',
            'password2': 'Check123#'
        }

        self.invalid_data_signup = {
            'email': 'eh',
            'username': 'eh',
            'password1': 'Check123#',
            'password2': 'diff'
        }

        self.user = User.objects.create_user(username='testuser', password='Check123#')

    def test_login_form_valid(self):
        """Test valid LoginForm submission"""
        form = LoginForm(data=self.valid_data_login)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        """Test invalid LoginForm submission"""
        form = LoginForm(data=self.invalid_data_login)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)

    def test_signup_form_valid(self):
        """Test valid SignupForm submission"""
        form = SignupForm(data=self.valid_data_signup)
        self.assertTrue(form.is_valid())


    def test_signup_form_invalid(self):
        """Test invalid SignupForm submission"""
        form = SignupForm(data=self.invalid_data_signup)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
