from django.urls import path
from . import views

urlpatterns = [
    path('add_brands/', views.add_brands, name='add_brands'),
    path('delete_brand', views.delete_brand, name='delete_brand'),
]
