from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from .models import Store
from django.http import JsonResponse

# Latitude= 0.3217912
# Longitude= 32.5512277

# user_location = fromstr("POINT" + "("+str(Longitude)+" "+str(Latitude)+")", srid=4326)


# class StoreListView(generic.ListView):
#     model = Store
#     context_object_name = 'stores'
#     queryset = Store.objects.annotate(distance=Distance('location', user_location)).order_by('distance')[:6]
#     template_name = 'store/store-list.html'


def store_list(request):
    if request.method == 'POST':
        latitude = request.POST.get('lat', None)
        longitude = request.POST.get('long', None)
        user_location = fromstr("POINT" + "("+str(longitude)+" "+str(latitude)+")", srid=4326)
        queryset = Store.objects.annotate(distance=Distance('location', user_location)).order_by('distance')[:6]
        context = {
            'stores': queryset
        }
        print(latitude, longitude)
        return render(request, 'store/index.html', context)
    else:
        return render(request, 'store/index.html')
    