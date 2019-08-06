from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse

LABEL_CHOICES = (
    ('S', 'Sale'),
    ('B', 'Back to School'),
)

class Item(models.Model):
    title = models.CharField(max_length=25)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    slug = models.SlugField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(verbose_name="Categories")
    label = models.CharField(choices=LABEL_CHOICES, blank=True, null=True, max_length=2)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:item_detail', args=[
            self.slug
        ])

    def get_add_to_cart_url(self):
        return reverse('shop:add_to_cart', args=[
            self.slug
        ])

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    created = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

