from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.http import HttpResponse
from .models import BlogPost
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    """
    Simply renders the index.html file which contains content for the home page
    """

    return render(request, 'blogs/index.html', {'page' : 'Home'})

def about_page (request):
    """
    Simply renders the about.html file which contains content for the about page
    """
    
    return render(request, 'blogs/about.html', {'page' : 'About Us'})


def blog_show(request):
    """
    Handles the logic to show all the blog posts. 
    Anyone can view the posts
    """

    my_posts = request.GET.get('mine')

    if my_posts:
        blogs = BlogPost.objects.filter(user = request.user)
    else:
        blogs = BlogPost.objects.all()
    return render (request, "blogs/blogs_show.html", {'blogs' : blogs})



@login_required
def blog_create(request):
    """
    Handles the logic to create a new blog post. 
    Only an authorised user can create a new blog.
    """

    if request.method == 'GET':
        context = {'form' : BlogCreationForm()}

        return render (request, 'blogs/blog_create.html', context)
    
    elif request.method == 'POST':
        form = BlogCreationForm(request.POST)
        if form.is_valid():
            blog_object = form.save(commit=False)
            blog_object.user = request.user
            blog_object.save()
            return redirect('/blog/')
    else:
        return render(request, 'blogs/blog_create.html', {'form': form})




@login_required
def blog_delete(request):
    """
    Handles the logic to delete a blog post using the Blog ID. 
    Only an authorised user can delete their blogs.
    """


    if request.method == 'GET':
        context = {'form' : BlogDeletionForm()}

        return render (request, 'blogs/blogs_delete.html', context)
    
    elif request.method == 'POST':
        form = BlogDeletionForm(request.POST)

        if (form.is_valid()):
            delete_id = form.cleaned_data['id']

            #Checks if the id entered even exists in the databse
            blog = BlogPost.objects.filter(id=delete_id)
            if not blog.exists():
                messages.error(request, f'Blog ID: {delete_id} does not exist')
                return redirect('/blog/delete/')
            
            #Checks if the blog's author is the logged in user
            if not check_ownership(request, delete_id):
                return redirect('/blog/delete/')

            try:
                BlogPost.objects.get(id = delete_id).delete()
                return redirect('/blog/')
            except BlogPost.DoesNotExist:
                messages.error(request, "This ID Blog doesn't exist. Enter a valid Blog ID")
                return redirect('/blog/delete/')

        else:
            return render (request, 'blogs/blogs_delete.html', {'form' : form})

        
@login_required
def blog_update(request):
    """
    Handles the logic to update a blog post using the Blog ID. 
    Only an authorised user can update their blogs.
    """

    if request.method == 'GET':
        context = {'form' : BlogUpdationForm}

        return render (request, 'blogs/blogs_update.html', context)
    
    elif request.method == 'POST':
        # Helper function 
        return update_post(request)



@login_required
def blog_update_button(request, update_id):
    """
    Handles the logic to update a blog post using the update button provided in the All Blogs Menu for each post. 
    Only an authorised user can update their blogs.
    """

    if not check_ownership(request, update_id):
        return redirect('/blog/')
    

    blog = BlogPost.objects.get(id=update_id)

    if request.method == 'GET':
        
        initial = {'id': blog.id, 'title': blog.title, 'content': blog.content}

        form = BlogUpdationForm(initial=initial)

        return render (request, 'blogs/blogs_update.html', {'form' : form})
    
    elif request.method == 'POST':
        return update_post(request)


@login_required
def blog_delete_button(request, delete_id):
    """
    Handles the logic to delete a blog post using the delete button provided in the All Blogs Menu for each post. 
    Only an authorised user can delete their blogs.
    """
    
    if not check_ownership(request, delete_id):
        return redirect('/blog/')

    try:
        BlogPost.objects.get(id=delete_id).delete()
        messages.success(request, f"Blog {delete_id} have been deleted")
        return redirect('/blog/')
    except Exception as e:
        messages.error(request, f"Error: {e}")


def update_post(request):

    """
    Helper function that provides the logic to update a blog using the Django form values. Used in functions 'blog_update' and 'blog_update_button'
    """

    form = BlogUpdationForm(request.POST)
    
    #Displays error if the form is not valid
    if not form.is_valid():
        messages.error(request, "Form is not valid. Enter valid details")
        return redirect('/blog/update/')
        
    
    update_id = form.cleaned_data['id']

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

def show_validation_form(request):
    if request.method == 'POST':
        # Just for test
        print(request.POST)
    return render(request, 'blogs/form.html')