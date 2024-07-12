# utils.py
from .models import Invoice
import json

def parse_and_create_models(json_data):
    data = json.loads(json_data)
    # Assuming the JSON data is a list of dictionaries
    for item in data:
        Invoice.objects.create(**item)
