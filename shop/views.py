from django.shortcuts import render

from .models import Item

# Create your views here.
def shop(request):
    items = Item.objects.order_by('-created')
    context = {
        'items': items
    }
    return render(request, "shop/shop.html", context)