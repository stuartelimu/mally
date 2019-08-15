from django.shortcuts import render
from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from .models import Store

Latitude= 0.3217912
Longitude= 32.5512277

user_location = fromstr("POINT" + "("+str(Longitude)+" "+str(Latitude)+")", srid=4326)


class StoreListView(generic.ListView):
    model = Store
    context_object_name = 'stores'
    queryset = Store.objects.annotate(distance=Distance('location', user_location)).order_by('distance')[:6]
    template_name = 'store/store-list.html'