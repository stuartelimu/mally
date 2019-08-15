from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.StoreListView.as_view(), name='store-list'),
    path('name/', views.getname, name='name'),
    
]

