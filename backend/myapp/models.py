from django.db import models

class Transaction(models.Model):
    TRANSACTION_TYPES = [('BUY', 'Buy'), ('SELL', 'Sell')]

    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    date = models.DateField()  # Storing date as a DateField
    time = models.TimeField()  # Storing time as a TimeField
    ticker_symbol = models.CharField(max_length=10)
    number_of_shares = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_share = models.DecimalField(max_digits=15, decimal_places=2)
    image_filename = models.CharField(max_length=100)
    transaction_valuation = models.DecimalField(max_digits=15, decimal_places=2)
    overall_holdings = models.DecimalField(max_digits=15, decimal_places=2)
    average_cost_per_share = models.DecimalField(max_digits=15, decimal_places=2)
    realized_gain_loss = models.DecimalField(max_digits=15, decimal_places=2)
    portfolio_valuation = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.ticker_symbol} ({self.transaction_type})"
