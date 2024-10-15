from django.urls import path
from orders.views import *

app_name = 'orders'

urlpatterns = [
    path("", my_orders, name="my-orders"),
    path("order-details/<oid>", order_details, name="order-details"),
    path("create-order/", create_order, name="create-order"),
    path("cancel-order/", cancel_order, name="cancel-order"),
    path("remove-order-item/", remove_order_item, name="remove-order-item"),
    
   
    

]
