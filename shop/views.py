from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Item, OrderItem, Order

# Create your views here.
def shop(request):
    items = Item.objects.order_by('-created')
    context = {
        'items': items
    }
    return render(request, "shop/shop.html", context)

def itemdetail(request, item):
    item = get_object_or_404(Item, slug=item)
    context = {
        'item': item,
    }
    return render(request, "shop/shop-single.html", context)

def add_to_cart(request, item):
    item = get_object_or_404(Item, slug=item)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user, ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        # size = request.get('shop-sizes')
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("shop:item_detail", item.slug)

def remove_from_cart(request, item):
    item = get_object_or_404(Item, slug=item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_item = OrderItem.objects.filter(
        item=item,
        user=request.user, ordered=False
    )[0]
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.remove(order_item)
    return redirect("shop:item_detail", item.slug)
