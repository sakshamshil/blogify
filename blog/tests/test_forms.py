from django.test import TestCase
from blog.forms import *

class TestForms(TestCase):
    def test_blog_creation_form_valid(self):
        form_data = {'title': 'Test Title', 'content': 'Test Content'}
        form = BlogCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blog_creation_form_invalid_missing_title(self):
        form_data = {'content': 'Test Content'}
        form = BlogCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_blog_deletion_form_valid(self):
        form_data = {'id': 5}
        form = BlogDeletionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blog_deletion_form_invalid_negative_id(self):
        form_data = {'id': -1}
        form = BlogDeletionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_blog_updation_form_valid_full_update(self):
        form_data = {'id': 3, 'title': 'Updated Title', 'content': 'Updated Content'}
        form = BlogUpdationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blog_updation_form_valid_partial_update(self):
        form_data = {'id': 3, 'title': 'Updated Title'}
        form = BlogUpdationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blog_updation_form_invalid_missing_id(self):
        form_data = {'title': 'Updated Title'}
        form = BlogUpdationForm(data=form_data)
        self.assertFalse(form.is_valid())
