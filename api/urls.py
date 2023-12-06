from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produk/', views.produk_list_api, name='list produk'),
    path('produk/<int:produk_id>', views.get_by_id, name='get produk'),
    path('produk/<int:produk_id>/delete', views.produk_delete, name='delete produk'),
    path('produk/<int:produk_id>/update', views.produk_update, name='update produk'),
    path('produk/create', views.produk_create, name='create produk'),
    path('kategori/', views.kategori_list, name='list kategori'),

]