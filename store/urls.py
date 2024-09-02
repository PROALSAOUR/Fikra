from django.urls import path
from store.views import *

app_name = 'store'

urlpatterns = [
    path("", index, name="home"),
    path("brand/<int:id>/", brand_page, name="brand"),
    path("category/<int:id>/", category_page, name="category"),
]
