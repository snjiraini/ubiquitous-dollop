from django.urls import path
from . import views
from .views import homepage, client_bid_page

urlpatterns = [
    path('', homepage, name='homepage'),  # Homepage
    path('place-bid/', client_bid_page, name='client_bid_page'),  # Client Bidding Page
]
