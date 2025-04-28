from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name = 'home'),
    path('about/', about_page, name = 'about'),
    path('blog/', blog_show, name = 'show'),
    path('blog/create/', blog_create, name = 'create'),
    path('blog/delete/', blog_delete, name = 'delete'),
    path('blog/update/', blog_update, name = 'update'),
    path('blog/delete/<int:delete_id>/', blog_delete_button, name = 'delete_button'),
    path('blog/update/<int:update_id>/', blog_update_button, name = 'update_button'),
    # path('validate/', show_validation_form, name='velo_form'),

]