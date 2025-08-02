# categories/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list_create_view),
]