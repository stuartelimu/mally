from django.urls import path, include
from .views import profile

app_name='accounts'

urlpatterns = [
    path('profile/', profile, name='profile'),
    
]

