import json
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path

def load_transactions(request):
    json_file_path = Path(settings.BASE_DIR) / 'data' / 'investments_data.json'
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return JsonResponse(data, safe=False)
