from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import BlogPost
from django.contrib.auth.decorators import login_required
from .helper import *
from django.core.paginator import Paginator


def home(request):
    try:
        return render(request, 'blogs/index.html', {'page': 'Home'})
    except Exception as e:
        messages.error(request, f"Error occured {e}")
        return redirect('/')

def about_page(request):
    try:
        return render(request, 'blogs/about.html', {'page': 'About Us'})
    except Exception as e:
        messages.error(request, f"Error occured {e}")
        return redirect('/')

def blog_show(request):
    try:
        my_posts = request.GET.get('mine')
        if request.user.is_authenticated and my_posts:
            blogs = BlogPost.objects.filter(user=request.user)
        else:
            blogs = BlogPost.objects.all()

        paginator = Paginator(blogs, 5) 
        page_number = request.GET.get('page')
        blogs_per_page = paginator.get_page(page_number)

        return render(request, "blogs/blogs_show.html", {'blogs_per_page': blogs_per_page, 'page': 'Show Blogs'})
    except Exception as e:
        messages.error(request, f"Error occured {e}")
        return redirect('/')

@login_required
def blog_create(request):
    try:
        if request.method == 'GET':
            context = {'form': BlogCreationForm()}
            return render(request, 'blogs/blog_create.html', context)

        elif request.method == 'POST':
            form = BlogCreationForm(request.POST)
            if form.is_valid():
                blog_object = form.save(commit=False)
                blog_object.user = request.user
                blog_object.save()
                return redirect('/blog/')
            else:
                messages.error(request, "Invalid blog form")
        return render(request, 'blogs/blog_create.html', {'form': form, 'page': 'Create Blog'})
    except Exception as e:
        messages.error(request, f"Error occured {e}")
        return redirect('/blog/create/')

@login_required
def blog_delete(request):
    if request.method == 'GET':
        try:
            context = {'form': BlogDeletionForm(), 'page': 'Delete Blog'}
            return render(request, 'blogs/blogs_delete.html', context)
        except Exception as e:
            messages.error(request, f"Error occured {e}")
            return redirect('/blog/delete/')
    
    elif request.method == 'POST':
        form = BlogDeletionForm(request.POST)
        if form.is_valid():
            delete_id = form.cleaned_data['id']
            blog = BlogPost.objects.filter(id=delete_id)
            if not blog.exists():
                messages.error(request, f'Blog ID: {delete_id} does not exist')
                return redirect('/blog/delete/')
            elif not check_ownership(request, delete_id):
                return redirect('/blog/delete/')
            else:
                try:
                    BlogPost.objects.get(id=delete_id).delete()
                    return redirect('/blog/')
                except BlogPost.DoesNotExist:
                    messages.error(request, "This ID Blog doesn't exist. Enter a valid Blog ID")
                    return redirect('/blog/delete/')
        else:
            return render(request, 'blogs/blogs_delete.html', {'form': form, 'page': 'Delete Blog'})

@login_required
def blog_update(request):
    try:
        if request.method == 'GET':
            context = {'form': BlogUpdationForm, 'page': 'Update Blog'}
            return render(request, 'blogs/blogs_update.html', context)
        elif request.method == 'POST':
            return update_post(request)
    except Exception as e:
        messages.error(request, f"Error occured {e}")
        return redirect('/blog/')

@login_required
def blog_update_button(request, update_id):
    try:
        if not check_ownership(request, update_id):
            return redirect('/blog/')

        blog = BlogPost.objects.get(id=update_id)

        if request.method == 'GET':
            initial = {'title': blog.title, 'content': blog.content}
            form = BlogUpdationForm(initial=initial)
            context = {'form': form, 'blog_id': update_id, 'button_mode': True}
            return render(request, 'blogs/blogs_update.html', context)

        elif request.method == 'POST':
            return update_post(request, update_id)
    except BlogPost.DoesNotExist:
        messages.error(request, "Blog not found")
        return redirect('/blog/')
    except Exception as e:
        messages.error(request, f"Error occured {e}")
        return redirect('/blog/')

@login_required
def blog_delete_button(request, delete_id):
    try:
        if not check_ownership(request, delete_id):
            return redirect('/blog/')
        BlogPost.objects.get(id=delete_id).delete()
        messages.success(request, f"Blog {delete_id} have been deleted")
        return redirect('/blog/')
    except BlogPost.DoesNotExist:
        messages.error(request, "Blog not found")
        return redirect('/blog/')
    except Exception as e:
        messages.error(request, f"Error occured {e}")
        return redirect('/blog/')
