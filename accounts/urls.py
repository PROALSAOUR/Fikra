from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path("", main_account_page, name="account_page"),
    path("account-info/", account_info, name="account_info"),
    path("sign/", sign, name="sign"),
    path('delete-account/', delete_account, name='delete_account'),
]
