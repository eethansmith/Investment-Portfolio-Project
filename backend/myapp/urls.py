from django.urls import path
from .views import get_stock_holdings

urlpatterns = [
    path('stock_holdings/', get_stock_holdings, name='stock_holdings'),
]
