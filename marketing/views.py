from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
import json
import requests
from .forms import EmailSignupForm
from .models import NewsLetter
from django.contrib import messages

def subscribe(email):
    SEND_GRID_API_KEY = settings.SEND_GRID_API_KEY

    base_api_url = 'https://api.sendgrid.com/v3/'
    headers = {'authorization': 'Bearer {0}'.format(SEND_GRID_API_KEY)}

    api_url = f"{base_api_url}marketing/contacts"
    list_id = "1a3c4c9c-16f8-4220-9f61-1e9d01b9f2de"

    payload = {"list_ids": [list_id], "contacts": [{"email": email}]}

    response = requests.put(api_url, json=payload, headers=headers)

    return response.status_code

def email_list_signup(request):
    form = EmailSignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email_signup_qs = NewsLetter.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.error(request, "You are already subscribed")
            else:
                subscribe(form.instance.email)
                form.save()
                messages.info(request, "Thank you for subscribing to our newsletter")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    
