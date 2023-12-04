import json
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path
import yfinance as yf
import pytz
from datetime import datetime

# Your timezone, for example, 'UTC'
timezone = pytz.timezone('EST')

