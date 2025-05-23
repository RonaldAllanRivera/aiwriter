from django.urls import path
from .views import generate_view, history_view

urlpatterns = [
    path("generate/", generate_view, name="generate"),
    path("history/", history_view, name="history"),
]