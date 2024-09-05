from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', blog, name='blog'),
    path('blog-page/<slug:slug>/', page_details, name='page-details'),
    path('questions/', questions_page, name='questions-page'),
]
