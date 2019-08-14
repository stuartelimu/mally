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

from .models import Item, OrderItem, Order, Address, Coupon
from .forms import CheckoutForm, CouponForm

import random
import string

def generateRef(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_uppercase + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

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


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order
            }

            billing_address_qs = Address.objects.filter(
                user = self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]}
                )

            shipping_address_qs = Address.objects.filter(
                user = self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]}
                )

            return render(self.request, "shop/checkout.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Order does not exist")
            return redirect("shop:checkout")
        

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_billing = form.cleaned_data.get('use_default_billing')
                if use_default_billing:
                    print("using default billing address")
                    billing_address_qs = Address.objects.filter(
                        user = self.request.user,
                        address_type='B',
                        default=True
                    )
                    if billing_address_qs.exists():
                        billing_address = billing_address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.error(self.request, "No default billing address")
                        return redirect("shop:checkout")
                else:
                    print("user is entering billing address")

                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    country = form.cleaned_data.get('billing_country')
                    zip = form.cleaned_data.get('billing_zip')
                    
                    if is_valid_form([billing_address1, country, zip]):
                        billing_address = Address(
                            user = self.request.user,
                            street_address = billing_address1,
                            apartment_address = billing_address2,
                            country = country,
                            zip = zip,
                            address_type='B'
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()
                    else:
                        messages.info(self.request, "Please fill in all the required billing address fields")

                
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                same_shipping_address = form.cleaned_data.get('same_shipping_address')

                if not same_shipping_address:
                    shipping_address = billing_address
                    shipping_address.pk = None
                    shipping_address.save()
                    shipping_address.address_type = 'S'
                    shipping_address.save()
                    order.shipping_address = shipping_address
                    order.save()
                elif use_default_shipping:
                    print("using default shipping address")
                    shipping_address_qs = Address.objects.filter(
                        user = self.request.user,
                        address_type='S',
                        default=True
                    )
                    if shipping_address_qs.exists():
                        shipping_address = shipping_address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.error(self.request, "No default shipping address")
                        return redirect("shop:checkout")
                else:
                    print("user is entering shipping address")

                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    country = form.cleaned_data.get('shipping_country')
                    zip = form.cleaned_data.get('shipping_zip')
                    
                    if is_valid_form([shipping_address1, country, zip]):
                        shipping_address = Address(
                            user = self.request.user,
                            street_address = shipping_address1,
                            apartment_address = shipping_address2,
                            country = country,
                            zip = zip,
                            address_type='S'
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(self.request, "Please fill in all the required shipping address fields")
                


                payment_option = form.cleaned_data.get('payment_option')
                order.ref_code = generateRef(20)
                order.save()
                
                self.request.session['ref_code'] = order.ref_code
                # return redirect('process_payment')
                if payment_option == 'P':
                    return redirect("shop:payment")
                elif payment_option == 'M':
                    # return redirect("shop:payment", payment_option='momopay')
                    pass
                else:
                    messages.error(self.request, "Invalid option selected")
                    return redirect("shop:checkout")
        except ObjectDoesNotExist:
            messages.error(self.request, "Your cart is empty")
            return redirect("shop:order_summary")


def payment(request):
    return render(request, "shop/thankyou.html")