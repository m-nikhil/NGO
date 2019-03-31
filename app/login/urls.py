from django.urls import path, re_path, include
from . import views

urlpatterns = [ 
    path('login', views.LoginViewSet.as_view()),
    path('register', views.RegisterViewSet.as_view()),

    path('profile', views.UserProfileViewSet.as_view())
]

