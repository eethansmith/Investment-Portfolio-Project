from django.urls import path
from .current_stock_holdings import get_stock_holdings
from .current_stock_holdings_day import get_stock_holdings_day
from .graph_stock_holdings import get_stock_history
from .graph_stock_holdings_day import get_stock_history
from .historic_stock_holdings import get_historic_stock_holdings
from .graph_all_holdings import get_portfolio_value

urlpatterns = [
    path('stock_holdings/', get_stock_holdings, name='stock_holdings'),
    path('stock_holdings_day/', get_stock_holdings_day, name='stock_holdings_day'),
    path('graph_stock/<str:ticker>/', get_stock_history, name='graph_stock'),
    path('graph_stock_day/<str:ticker>/', get_stock_history, name='graph_stock_day'),
    path('historic_holdings/', get_historic_stock_holdings, name='all_holdings'),
    path('graph_portfolio/<int:days>/', get_portfolio_value, name='graph_portfolio'),
]