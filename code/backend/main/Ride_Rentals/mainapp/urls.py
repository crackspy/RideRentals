from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('auth/', views.auth_page, name='auth'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.index_home, name='index_home'),

    path('test/', views.test, name='test'),

]
