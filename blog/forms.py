from django import forms

from .models import BlogPost

class BlogCreationForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']
    
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'data-rule-required': 'true'
        })
    )

    

class BlogDeletionForm(forms.Form):
    id = forms.IntegerField(min_value = 1)
    

class BlogUpdationForm(forms.Form):
    id = forms.IntegerField(min_value = 1, label='Enter ID of the Blog to Update')
    title = forms.CharField(max_length = 100, required=False, empty_value=None)
    content = forms.CharField(required=False, empty_value=None, widget=forms.Textarea)