from django import template
from shop.models import Order, Item
from taggit.models import Tag

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

@register.simple_tag
def item_count():
	return Item.objects.all().count()

@register.filter
def tag_item_count(tag_slug):
	tag = Tag.objects.get(slug=tag_slug)
	items = Item.objects.filter(tags__in=[tag])
	return items.count()