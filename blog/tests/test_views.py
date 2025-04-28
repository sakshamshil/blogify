from django.test import TestCase, Client
from django.urls import reverse
from blog import models, views
import json
from django.contrib.auth.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client=Client()
        self.home_url = reverse('home')
        self.about_url = reverse('about')
        self.show_url = reverse('show')
        self.create_url = reverse('create')
        self.delete_url = reverse('delete')
        self.update_url = reverse('update')
        #dummy user to login
        self.user = User.objects.create_user(username='testuser', password='Testpass1')
        #dummy post
        self.blog =  models.BlogPost.objects.create(title='Test Blog', content='Test Content', user=self.user)
        self.delete_button_url = reverse('delete_button', args=[self.blog.id])
        self.update_button_url = reverse('update_button', args=[self.blog.id])



    def test_home_GET(self):
        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/index.html')


    def test_about_GET(self):
        response = self.client.get(self.about_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/about.html')


    def test_show_GET(self):
        response = self.client.get(self.show_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogs_show.html')

    
    def test_create_GET(self):
        response = self.client.get(self.create_url)
        #Checks if redirects to login before logging in
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=' + self.create_url)

        # Login using dummy data
        self.client.login(username='testuser', password='Testpass1')
        response = self.client.get(self.create_url)

        
        #Checks if create page opens after logging in
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blog_create.html')

    

    
    def test_update_GET(self):
        response = self.client.get(self.update_url)
        #Checks if redirects to login before logging in
        self.assertRedirects(response, '/login/?next=' + self.update_url)

        # Login using dummy data
        self.client.login(username='testuser', password='Testpass1')
        response = self.client.get(self.update_url)

        
        #Checks if the page opens after logging in
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogs_update.html')
        self.assertEqual(response.status_code, 200)




    def test_delete_POST (self):
        self.client.login(username='testuser', password='Testpass1')
        form_data = {'id': self.blog.id}

        response = self.client.post(self.delete_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog/')
        self.assertFalse(models.BlogPost.objects.filter(id=self.blog.id).exists())
        
    def test_delete_POST_invalid_id(self):
        self.client.login(username='testuser', password='Testpass1')
        form_data = {'id': 999999}
        response = self.client.post(self.delete_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog/delete/')    


    def test_update_POST (self):
        self.client.login(username='testuser', password='Testpass1')
        form_data = {'id': self.blog.id, 'title' : "Updated Title", 'content' : "Updated Content"}

        response = self.client.post(self.update_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog/')

        updated_blog = models.BlogPost.objects.get(id=self.blog.id)
        self.assertEqual(updated_blog.title, 'Updated Title')
        self.assertEqual(updated_blog.content, 'Updated Content')


    def test_update_POST_invalid_id(self):
        self.client.login(username='testuser', password='Testpass1')
        form_data = {'id': 999999}
        response = self.client.post(self.update_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog/update/')    


    def test_delete_button(self):
        self.client.login(username='testuser', password='Testpass1')
        response = self.client.get(self.delete_button_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog/')
        self.assertFalse(models.BlogPost.objects.filter(id=self.blog.id).exists())


    def test_blog_update_button_GET(self):
        self.client.login(username='testuser', password='Testpass1')
        response = self.client.get(self.update_button_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogs_update.html')
        self.assertContains(response, self.blog.title)
        self.assertContains(response, self.blog.content)
