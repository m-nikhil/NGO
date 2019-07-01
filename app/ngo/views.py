from django.shortcuts import render
from . import serializers
from .models import NgoDetail,Needs,City,CharityHomeType
from rest_framework import views, viewsets
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from login.permissions import SuperUserPermission, NgoPermission
from . import filters
from django_filters import rest_framework as django_filters
from rest_framework.permissions import AllowAny

class NgoProfileViewSet(views.APIView):

    permission_classes = [NgoPermission]

    def get(self, request):

        ngoDetails = NgoDetail.objects.get(pk=request.user)
        serializer = serializers.NgoProfileSerializer(ngoDetails)
        
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.NgoProfileSerializer)
    def put(self, request, pk=None):

        ngoDetails = NgoDetail.objects.get(pk=request.user)

        serializer = serializers.NgoProfileSerializer(ngoDetails,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'msg': 'User profile successfully updated'}, status=HTTP_200_OK)


class AddNeedsViewSet(viewsets.ModelViewSet):

    permission_classes = [NgoPermission]
    serializer_class = serializers.NeedsSerializer
    http_method_names = ['post','put']

    def get_queryset(self):
        return Needs.objects.filter(ngo = self.request.user.ngo)
    
    def get_serializer_context(self):
        return {'request': self.request}



class NgoViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.NgoDetailsSerializer
    http_method_names = ['get']
    queryset = NgoDetail.objects.all()

    filterset_class = filters.NgoFilter
    filter_backends = (django_filters.DjangoFilterBackend,)

class CityViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.CitySerializer
    http_method_names = ['get']
    queryset = City.objects.all()

class CharityHomeTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.CharityHomeTypeSerializer
    http_method_names = ['get']
    queryset = CharityHomeType.objects.all()   


