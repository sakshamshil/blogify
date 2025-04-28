from django.urls import reverse, resolve
from django.test import SimpleTestCase
from users import views


class TestUrls(SimpleTestCase):
    """
    This tester class is used to test various url paths. They assert if the urls are mapped to the views they are intended to.
    """

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.sign_in)


    def test_register_url(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, views.signup)

    
    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.sign_out)
