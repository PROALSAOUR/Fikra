from django.urls import path
from orders.views import *

app_name = 'orders'

urlpatterns = [
    path("", my_orders, name="my-orders"),
    path('admin/orders/<int:order_id>/print/', print_invoice_view, name='print_invoice'),
    path("order-details/<oid>", order_details, name="order-details"),
    path("create-order/", create_order, name="create-order"),
    path("edit-order/", edit_order, name="edit-order"),
    path("cancel-order/", cancel_order, name="cancel-order"),
    path("remove-order-item/", remove_order_item, name="remove-order-item"),
    path("dealing/<oid>", order_dealing, name="order-dealing"),
]
