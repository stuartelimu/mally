from django.urls import path
from . import views

app_name='shop'

urlpatterns = [
    path('shop/', views.shop),
    path('shop/category/<slug:tag_slug>/', views.shop, name='item_list_by_category'),
    path('shop/<slug:item>/', views.itemdetail, name="item_detail"),
    path('shop/add-to-cart/<slug:item>/', views.add_to_cart, name="add_to_cart"),
    path('shop/remove-to-cart/<slug:item>/', views.remove_from_cart, name="remove_to_cart"),

]

