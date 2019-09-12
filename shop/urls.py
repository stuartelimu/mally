from django.urls import path
from . import views

app_name='shop'

urlpatterns = [
    path('shop/', views.shop, name="item_list"),
    path('shop/category/<slug:tag_slug>/', views.shop, name='item_list_by_category'),
    path('shop/<slug:item>/', views.itemdetail, name="item_detail"),
    path('shop/add-to-cart/<slug:slug>/', views.add_to_cart, name="add_to_cart"),
    path('shop/remove-from-cart/<slug:slug>/', views.remove_from_cart, name="remove_from_cart"),
    path('cart/', views.OrderSummaryView.as_view(), name='cart'),
    path('cart/<slug:slug>/remove_single_item_from_cart/', views.remove_single_item_from_cart, name="remove_single_item_from_cart"),
    path('cart/<slug:slug>/add_single_item_to_cart/', views.add_single_item_to_cart, name="add_single_item_to_cart"),
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
    path('payment/<payment_option>/', views.process_paypal_payment, name="paypal_payment"),
    path('payment_done/', views.payment_done, name="payment_done"),
    path('payment_cancelled/', views.payment_canceled, name="payment_cancelled"),
    path('add_coupon/', views.AddCouponView.as_view(), name="add_coupon"),
    path('request-refund/', views.RequestRefundView.as_view(), name='request-refund'),

]

