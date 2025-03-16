from django.urls import path
from store.views import *

app_name = 'store'

urlpatterns = [
    path("", index, name="home"),
    
    path('serviceworker.js', service_worker, name='service_worker'),
    
    path('offline/', offline, name='offline'),
    
    path("brand/<slug:slug>/", brand_page, name="brand"),
    
    path("category/<slug:slug>/", category_page, name="category"),
    
    path("ad-details/<slug:slug>/", ads_page, name="ad_details"),
    
    path("offer/", offer_page, name="offer_page"),
    
    path("best-sales/", best_sales, name="best-sales"),
        
    path("search/", search_page, name="search_page"),
    
    path("favourite/", favourite_page, name="favourite_page"),
    path('add-to-favourites/<int:product_id>/', add_to_favourites, name='add_to_favourites'),
    path('favourite/clear/', clear_favourites, name='clear_favourites'),
    
    path("product/<pid>", product_details, name="product_details"),
    path('get-stock/', get_stock, name='get_stock'),  # مسار لجلب المخزون الخاص بالمنتج
    
    path('cart/', cart_page, name='cart_page'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('add-to-cart2/<str:pid>/', add_to_cart2, name='add_to_cart2'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart-item-qty/', update_cart_item_qty, name='update_cart_item_qty'),
    

]
