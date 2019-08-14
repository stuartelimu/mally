from django.contrib import admin
from .models import Order, OrderItem, Item, Address, Coupon

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)

