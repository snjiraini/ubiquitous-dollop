from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bonds, name='view_bonds'),  # Default page for bonds
    path('bid/<int:bond_id>/', views.place_bid, name='place_bid'),  # Page to place a bid
]
