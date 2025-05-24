from django.contrib import admin
from django.urls import path, include
from generator.views import home_view

urlpatterns = [
    path("", home_view, name="home"),
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),  # AllAuth entry point
    path("", include("generator.urls")),
]
