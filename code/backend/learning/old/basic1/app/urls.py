"""
URL configuration for basic1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page),
    path('print-hello/', views.print_hello, name='print_hello'),
    path('hello/', views.hello_page, name='hello'),
    path('one/', views.one_page, name='one'),
    path('image/', views.show_image, name='image'),
    path('crud/', views.crud, name='crud'),
    path('crud/create/', views.crud_create, name='create'),
    path('crud/delete/', views.crud_delete, name='delete'),
    path('crud/modify/', views.crud_modify, name='modify'),
    path('crud/update/', views.crud_update, name='update')

]
