from django.urls import path
from . import views

app_name='shop'

urlpatterns = [
    path('shop/', views.shop),
    path('shop/<slug:item>/', views.itemdetail, name="item_detail"),
    path('shop/add-to-cart/<slug:item>/', views.add_to_cart, name="add_to_cart"),

]

