from django.urls import path
from . import views

app_name='shop'

urlpatterns = [
    path('shop/', views.shop, name="item_list"),
    path('shop/category/<slug:tag_slug>/', views.shop, name='item_list_by_category'),
    path('shop/<slug:item>/', views.itemdetail, name="item_detail"),
    path('shop/add-to-cart/<slug:item>/', views.add_to_cart, name="add_to_cart"),
    path('shop/remove-from-cart/<slug:item>/', views.remove_from_cart, name="remove_from_cart"),
    path('cart/', views.OrderSummaryView.as_view(), name='cart'),
    path('cart/<slug:slug>/remove_single_item_from_cart/', views.remove_single_item_from_cart, name="remove_single_item_from_cart"),
    path('cart/<slug:slug>/add_single_item_to_cart/', views.add_single_item_to_cart, name="add_single_item_to_cart"),

]

