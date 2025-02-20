from django.urls import path
from cards.views import *

app_name = 'cards'

urlpatterns = [
    
    path('', cards_repo, name='cards-repo'),
    path('cards-store/', cards_store, name='cards-store'),
    path('copon-details/<cid>', copon_details, name='copon-details'),
    path('buy-copon/<cid>', buy_copon, name='buy-copon'),
    path('verfie-code/', verfie_code, name='verfie-code'),
        
]
