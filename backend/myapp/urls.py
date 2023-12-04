from django.urls import path
from .current_stock_holdings import get_stock_holdings
from .graph_stock_holdings import get_stock_history

urlpatterns = [
    path('stock_holdings/', get_stock_holdings, name='stock_holdings'),
    path('graph_stock/<str:ticker>/', get_stock_history, name='graph_stock'),
]