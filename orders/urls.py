from django.urls import path
from orders.views import *

app_name = 'orders'

urlpatterns = [
    path("create-order/", create_order, name="create-order"),
    
   
    

]
