from django.shortcuts import render, redirect

from django.conf import settings
from .forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail

def sign_in(request):
    """
    Handles the logic for user sign in page.
    """
    
    try:
        # if there is a user already logged in and tries to access the signin page, it redirects to the home page
        if request.user.is_authenticated:
            return redirect('/')

        if request.method == 'GET':
            form = LoginForm()
            return render(request, 'users/login.html', {'form': form, 'page': 'Login'})

        elif request.method == 'POST':
            form = LoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
            
                user = authenticate(request, username=username, password=password)

                if user:
                    login(request, user)
                    messages.success(request, f'Hi, {username.title()}, welcome back!')
                    return redirect('/')
            
                else:
                    messages.error(request, 'Invalid credentials. Signup if you are a new user!')
                    return render(request, 'users/login.html', {'form': form})
            else :
                messages.error(request, 'Invalid Entries.')
                return render(request, 'users/login.html', {'form': form, 'page' : 'Login'})
        
    except Exception as e:
        messages.error(request, f'Error: {e}')
        return redirect('/')


def signup(request):
    try:
        if request.user.is_authenticated:
            return redirect('/')

        if request.method == 'GET':
            form = SignupForm()
            return render(request, 'users/register.html', {'form': form, 'page': 'Register'})

        elif request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']

                messages.success(request, 'User created successfully! Check your inbox.')

                send_mail(
                    "Blogify Account Created. Congratulations!",
                    f"Hi {username}, your Blogify account has been created successfully. Head to the login page and start writing content now!",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                )

                return redirect('/login/')
            else:
                messages.error(request, "Signup failed! Try again")
                return render(request, 'users/register.html', {'form': form, 'page': 'Register'})
    except Exception as e:
        messages.error(request, f'Error: {e}')
        return redirect('/')

    

def sign_out(request):
    """
    Handles the logic for sign out for a logged in user.
    """
    try:
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('/login/')
    except Exception as e:
        messages.error(request, f'Logout error: {str(e)}')
        return redirect('/')
    

    