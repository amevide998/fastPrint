# frontend/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('produk-list/', views.produk_list, name='produk-list'),
]
