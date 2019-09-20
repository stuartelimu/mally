from django.shortcuts import render
from shop.models import Order


# Create your views here.
def profile(request):
    last_order = Order.objects.filter(user=1, ordered=True).order_by('-ordered_date')[0]
    return render(request, 'accounts/profile.html', {'last_order':last_order})
    