from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path("", main_account_page, name="account_page"),
    path("account-info/", account_info, name="account_info"),
    path('mark-as-read/<int:message_id>/', mark_as_read, name='mark-as-read'),
    path("sign/", sign, name="sign"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path("choose-city/", choose_city, name="choose-city"),
    path('delete-account/', delete_account, name='delete_account'),
    path('edit-account/name/', edit_name, name='edit-name'),
    path('edit-account/password/', edit_account, name='edit-password'),
    path('edit-account/password/forget-password', forget_password, name='forget_password'),
    path('edit-account/password/enter-phone-number', phone_number_of_forgeted_password, name='phone_number_of_forgeted_password'),
    path('edit-account/password/verify-forget-password', verify_forget_password, name='verify_forget_password'),
    path('edit-account/password/reset-password', reset_password, name='reset_password'),
]
