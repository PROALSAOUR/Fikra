from django.urls import path
from store.views import *

app_name = 'store'

urlpatterns = [
    path("", index, name="home"),
    path("brand/<slug:slug>/", brand_page, name="brand"),
    path("category/<slug:slug>/", category_page, name="category"),
    path("ad-details/<slug:slug>/", ads_page, name="ad_details"),
    path("offer/", offer_page, name="offer_page"),
    path("search/", search_page, name="search_page"),
    path("product/<pid>", product_details, name="product_details"),
    path('get-stock/', get_stock, name='get_stock'),  # مسار لجلب المخزون الخاص بالمنتج

    ]
