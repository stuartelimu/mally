from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils import timezone
from taggit.models import Tag

from .models import Item, OrderItem, Order

# Create your views here.
def shop(request, tag_slug=None):
    items = Item.objects.order_by('-created')
    cats = Tag.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        items = items.filter(tags__in=[tag])

    paginator = Paginator(items, 8)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context = {
        'items': items,
        'tag': tag,
        'page': page,
        'cats': cats
    }
    return render(request, "shop/shop.html", context)

def itemdetail(request, item):
    item = get_object_or_404(Item, slug=item)
    item_tags_ids = item.tags.values_list('id', flat=True)
    similar_items = Item.objects.filter(tags__in=item_tags_ids).exclude(id=item.id)
    similar_items = similar_items.annotate(same_tags=Count('tags')).order_by('-same_tags')[:6]
    context = {
        'item': item,
        'similar_items': similar_items
    }
    return render(request, "shop/shop-single.html", context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
            }
            return render(self.request, 'shop/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Your cart is empty")
            return redirect("/")



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
    if order_qs.exists():
        order = order_qs[0]
        # check if the orderitem is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item, created = OrderItem.objects.get_or_create(
                item=item,
                user=request.user,
                ordered=False
            )
            order.items.remove(order_item)
            messages.info(request, "Item was removed from your cart")
            # return redirect("shop:order_summary")
    return redirect("shop:cart")

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the orderitem is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item, created = OrderItem.objects.get_or_create(
                item=item,
                user=request.user,
                ordered=False
            )
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "Item quantity was updated")
            else: 
                order.items.remove(order_item)
            return redirect("shop:cart")
    
@login_required
def add_single_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the orderitem is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item was updated to cart successfully")
            return redirect("shop:cart") 
