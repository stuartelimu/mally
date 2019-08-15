from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('stores/', views.get_store_list, name='get_store_list'),
    path('', views.store_list, name='store-list'),
    
]

