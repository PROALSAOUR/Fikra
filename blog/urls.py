from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', blog, name='blog'),
    path('blog-page/<id>', page_details, name='page-details'),
    path('qustions/', question_page, name='qustions-page'),
]
