from django.shortcuts import redirect
from django.contrib import messages
from .forms import *
from .models import BlogPost



def update_post(request, button_update_id=None):

    """
    Helper function that provides the logic to update a blog using the Django form values. Used in functions 'blog_update' and 'blog_update_button'
    """

    form = BlogUpdationForm(request.POST)
    
    #Displays error if the form is not valid
    if not form.is_valid():
        messages.error(request, "Form is not valid. Enter valid details")
        return redirect('/blog/update/')
        
    
    if button_update_id:
        update_id = button_update_id
    else:
        update_id = form.cleaned_data.get('id')

    #Checks if the id entered even exists in the databse
    blog = BlogPost.objects.filter(id=update_id)
    if not blog.exists():
        messages.error(request, f'Blog ID: {update_id} does not exist')
        return redirect('/blog/update/')


    #Checks if the blog's author is the logged in user
    if not check_ownership(request, update_id):
        return redirect('/blog/update/')
    

    title = form.cleaned_data['title']
    content = form.cleaned_data['content']

    
    update = {}
    if title: 
        update['title'] = title
    if content:
        update['content'] = content


    try:
        if update:
            blog.update(**update)
            messages.success(request, "Blog updated successfully!")
            return redirect('/blog/')
        else:
            messages.error(request, "Enter some changes. Can't leave all fields blank.")
            return redirect('/blog/update/')
                   
    except Exception as e:
        messages.error(request, f"Error -> {e}")
        return redirect('/blog/update/')
    


def check_ownership(request, id):
    """
    Helper function that is used in multiple places to check if the queried blog id belongs to the logged in user

    Returns:
        boolean: returns True if the blog's foreign key 'user' is the same as logged in user. False otherwise.
    """

    blog = BlogPost.objects.get(id=id)
    
    if blog.user != request.user:
        messages.error(request, f"You are not the author of Blog {id}")
        return False
    return True

