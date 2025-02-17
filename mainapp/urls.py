# Built by crackspy

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Homepage URL
    path('', views.index, name='home'),

    # Authentication URLs
    path('auth/', views.auth_page, name='auth'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    # Password reset URLs
    path(
        'password_reset/', 
        views.CustomPasswordResetView.as_view(template_name='mainapp/login/password_reset.html'), 
            name='password_reset'
        ),
    path(
        'password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='mainapp/login/password_reset_done.html'), 
            name='password_reset_done'),
    path(
        'password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='mainapp/login/password_reset_confirm.html'), 
            name='password_reset_confirm'),
    path(
        'password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='mainapp/login/password_reset_complete.html'), 
            name='password_reset_complete'),

    # User profile URLs
    path('profile/', views.profile_dashboard, name='profile'),
    path('profile/change_password/',
         auth_views.PasswordChangeView.as_view(template_name='mainapp/profile/change_password.html'),
         name='change_password'),
    path('profile/change_password/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='mainapp/profile/change_password_done.html'),
        name='password_change_done'),
    path('profile/update/', views.update_profile, name='update_profile'),

    # Car rental URLs
    path('cars/', views.explore_cars, name='explore_cars'),
    path('success/', views.success_page, name="success_page"),
    path('booking/<slug:slug>', views.booking, name='booking'),
    path('confirm_booking/<slug:slug>/', views.confirm_booking, name='confirm_booking'),
    path('payment_success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('add-to-wishlist/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<slug:slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),

]
