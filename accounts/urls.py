from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path("", main_account_page, name="account_page"),
    path("sign/", sign, name="sign"),
]
