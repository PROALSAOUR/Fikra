from django.urls import path
from cards.views import *

app_name = 'cards'

urlpatterns = [
    
    path('', cards_repo, name='cards-repo'),
    path('cards-store/', cards_store, name='cards-store'),
    path('gift-details/<gid>', gift_details, name='gift-details'),
    path('copon-details/<cid>', copon_details, name='copon-details'),
    path('buy-copon/<cid>', buy_copon, name='buy-copon'),
    path('buy-gift/<gid>', buy_gift, name='buy-gift'),
    path('buy-gift2/<gid>', buy_gift2, name='buy-gift2'),
    
]
