from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail

class TestViews(TestCase):

    def setUp(self):
        #TEST USER
        self.test_user = User.objects.create_user(username='testuser', password='Check123#')
        
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.logout_url = reverse('logout')

    def test_sign_in_get_authenticated(self):
        """ Test that an authenticated user is redirected from login page """
        self.client.login(username='testuser', password='Check123#')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, '/')  # Ensures redirect to home page

    def test_sign_in_get(self):
        """ Test GET request for sign in page """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_sign_in_post_invalid_credentials(self):
        """ Test POST request with invalid credentials """
        response = self.client.post(self.login_url, {'username': 'wronguser', 'password': 'wrongpass'})
        self.assertTemplateUsed(response, 'users/login.html')

    def test_sign_in_post_valid_credentials(self):
        """ Test POST request with valid credentials """
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'Check123#'})
        print(response.content)
        self.assertRedirects(response, '/')

    def test_signup_get(self):
        """ Test GET request for signup page """
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_signup_post_valid(self):
        """ Test POST request with valid data for signup """
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'Check123#',
            'password2': 'Check123#',
            'email': 'newtest@gmail.com'
        })
        self.assertRedirects(response, '/login/')
        self.assertEqual(len(mail.outbox), 1)  # Check if one email was sent
        self.assertIn("Blogify Account Created. Congratulations!", mail.outbox[0].subject)

    def test_signup_post_invalid(self):
        """ Test POST request with invalid data for signup """
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'eh',
            'password2': 'diff',
            'email': 'newtest@gmail.com'
        })
        self.assertTemplateUsed(response, 'users/register.html')

    def test_sign_out(self):
        """ Test sign out functionality """
        self.client.login(username='testuser', password='Check123#')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, '/login/')
