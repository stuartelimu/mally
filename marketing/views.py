from django.shortcuts import render
from django.conf import settings
import json
import requests

SEND_GRID_API_USER = settings.EMAIL_HOST_USER
SEND_GRID_API_KEY = settings.SEND_GRID_API_KEY

api_url = 'https://api.sendgrid.com/api/newsletter/lists/email/add.json'

def subscribe(email, name):
    data = {"email": email, "name": name}

    r = requests.post(
        api_url,
        api_user=SEND_GRID_API_USER,
        api_key=SEND_GRID_API_KEY,
        list='Mally newsletter',
        data=json.dumps(data)
    )

    return r.status_code, r.json

def email_list_signup(requests):
    pass
