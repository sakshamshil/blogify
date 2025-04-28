from django.test import TestCase
from blog.models import BlogPost
from django.contrib.auth.models import User

class TestModels(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Testpass1')
        self.blog = BlogPost.objects.create(
            title='Test Blog',
            content='Test Content',
            user=self.user
        )

    def test_blogpost_creation(self):
        self.assertEqual(self.blog.title, 'Test Blog')
        self.assertEqual(self.blog.content, 'Test Content')
        self.assertEqual(self.blog.user.username, 'testuser')