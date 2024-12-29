from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('auth/', views.auth_page, name='auth'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    path('cars/', views.explore_cars, name='explore_cars'),
    path('success/', views.success_page, name="success_page"),
    path('booking/<slug:slug>', views.booking, name='booking'),
    path('add-to-wishlist/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),


    path('test/', views.test, name='test'),

]
