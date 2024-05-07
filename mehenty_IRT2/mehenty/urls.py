from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),

    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('client/', views.client, name='client'),
    path('technicien/', views.technicien, name='technicien'),
]