from django.urls import path
from .views import *


urlpatterns = [
    path('login/', sign_in, name = 'login'),
    path('signup/', signup, name = 'signup'),
    path('logout/', sign_out, name = 'logout'),
]