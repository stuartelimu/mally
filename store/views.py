from django.shortcuts import render, redirect, reverse
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
        request.session['latitude'] = latitude
        request.session['longitude'] = longitude
        request.session.set_expiry(60)
        return redirect('store:store-list')
    else:
        try:
            latitude = request.session['latitude']
            longitude = request.session['longitude']
            if latitude != "" and longitude != "":
                user_location = fromstr("POINT" + "("+str(longitude)+" "+str(latitude)+")", srid=4326)
                queryset = Store.objects.annotate(distance=Distance('location', user_location)).order_by('distance')[:3]
                context = {
                    'stores': queryset
                }
                return render(request, 'store/index.html', context)
            else:
                return render(request, 'store/index.html')
        except KeyError:
            return render(request, 'store/index.html')

def index(request):
    return render(request, 'store/index.html')


def get_store_list(request):
    latitude = request.POST.get('lat', None)
    longitude = request.POST.get('long', None)
    user_location = fromstr("POINT" + "("+str(longitude)+" "+str(latitude)+")", srid=4326)
    queryset = Store.objects.annotate(distance=Distance('location', user_location)).order_by('distance')[:3]
    data = []

    store_name = ""
    store_distance = ""

    for store in queryset:
        store_distance = store.distance.m
        store_name = store.name
        store_dict = {"name": store_name, "distance": store_distance}
        data.append(store_dict)
    
    print(data)
    return JsonResponse(data, safe=False)

    