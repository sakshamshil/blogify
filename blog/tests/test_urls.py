from django.urls import reverse, resolve
from django.test import SimpleTestCase
from blog import views
from random import randint


class TestUrls(SimpleTestCase):
    """
    This tester class is used to test various url paths. They assert if the urls are mapped to the views they are intended to.
    """
    x = randint(1, 100)
    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)


    def test_show_url_is_resolved(self):
        url = reverse('show')
        self.assertEqual(resolve(url).func, views.blog_show)

    def test_create_url_is_resolved(self):
        url = reverse('create')
        self.assertEqual(resolve(url).func, views.blog_create)    

    def test_delete_url_is_resolved(self):
        url = reverse('delete')
        self.assertEqual(resolve(url).func, views.blog_delete)    

    def test_update_url_is_resolved(self):
        url = reverse('update')
        self.assertEqual(resolve(url).func, views.blog_update)    


    def test_about_url_is_resolved(self):
        url = reverse('about')
        self.assertEqual(resolve(url).func, views.about_page)

   
    def test_delete_button_url_is_resolved(self):
        url = reverse('delete_button', args=[self.x])
        self.assertEqual(resolve(url).func, views.blog_delete_button)

    def test_update_button_url_is_resolved(self):
        url = reverse('update_button', args=[self.x])
        self.assertEqual(resolve(url).func, views.blog_update_button)    

