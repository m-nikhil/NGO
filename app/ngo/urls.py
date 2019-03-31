from django.urls import path, re_path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('ngo', views.NgoViewSet)
router.register('profile/ngo/needs', views.AddNeedsViewSet, basename = "needs")

urlpatterns = [ 
    path('profile/ngo', views.NgoProfileViewSet.as_view()),
    path('', include(router.urls))
]

