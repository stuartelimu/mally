from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    # path('', views.StoreListView.as_view(), name='store-list'),
    path('', views.store_list, name='store-list'),
    
]

