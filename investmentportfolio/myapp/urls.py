from django.urls import path
from .views import load_transactions

urlpatterns = [
    path('transactions/', load_transactions, name='load_transactions'),
    # other paths...
]
