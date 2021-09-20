from django.urls import path
from .views import livefe, ReactView
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('camera', livefe, name='livefe'),
    path('wel/', ReactView.as_view(), name="something"),
]