from rest_framework import serializers
from .models import StockHolding  # Import your model

class StockHoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockHolding
        fields = ['id', 'name', 'quantity', 'value', 'imageUrl']  # Update with your model fields
