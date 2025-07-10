from django.urls import path
from .views import ProxyView

urlpatterns = [
    path('proxy/<str:service_name>/<path:subpath>', ProxyView.as_view(), name='proxy'),
]