from django.urls import path
from . import views

app_name = 'scrap'

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('list/', views.list_view, name='list_view'),
]
