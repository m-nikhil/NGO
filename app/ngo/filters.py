from django_filters import rest_framework as filters
from .models import NgoDetail
from django.db.models import Q
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.geoip2 import GeoIP2




    

class NgoFilter(filters.FilterSet):



    min_amountRaised = filters.NumberFilter(field_name="amountRaised", lookup_expr='gte')
    max_amountRaised = filters.NumberFilter(field_name="amountRaised", lookup_expr='lte')
    name = filters.CharFilter(lookup_expr='icontains')
    city = filters.CharFilter(field_name="city__city",lookup_expr='icontains')
    typeOfCharityHome = filters.CharFilter(field_name="charityHomeType__charityHomeType",lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')
    taxCertificate_boolean = filters.BooleanFilter( method='taxCertificate_not_empty')
    radius =  filters.NumberFilter( method='radius_filter' )



    class Meta:
        model = NgoDetail
        fields = ['name', 'city', 'typeOfCharityHome','address','taxCertificate_boolean']

        
    def radius_filter(self, queryset, name, value):

        g = GeoIP2()
        ip = self.request.META.get('REMOTE_ADDR', None)

        if(ip == "127.0.0.1"):
            lat = 13.0924544
            lng = 80.2209792
            point = Point(lng, lat)   
        else:
            point = g.geos(ip).wkt
            
        return queryset.filter(mapLocation__distance_lt=(point, Distance(km=value)))


    def taxCertificate_not_empty(self, queryset, name, value):
        if value == 1:
            return queryset.filter(taxCertificate__isnull=False).exclude(taxCertificate='')

        if value == 0:
            return queryset.filter(Q(taxCertificate__isnull=True) | Q(taxCertificate__exact=''))