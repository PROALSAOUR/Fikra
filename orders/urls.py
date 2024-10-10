from django.urls import path
from orders.views import *

app_name = 'orders'

urlpatterns = [
    path("my-orders/", my_orders, name="my-orders"),
    
   
    

]
