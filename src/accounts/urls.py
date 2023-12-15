from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.registration_view, name='registration_view'),
    path('update/', views.update_view, name='update_view'),
    path('delete/', views.delete_view, name='delete_view'),
]
