from django.contrib import admin
from django.template.loader import render_to_string
from .models import Profile, Car_info, Booking, Wishlist
from .utils import send_booking_email
# Register your models here.

# Custom action for marking booking as completed
def mark_as_completed(modeladmin, request, queryset):
    for booking in queryset:
        if booking.status != Booking.Status.COMPLETED:
            booking.status = Booking.Status.COMPLETED
            booking.payment_status = Booking.Payment_Status.PAID
            booking.car.available = True  # Make car available again
            booking.car.save()  # Save the updated car availability
            booking.save()  # Save the booking with updated status

mark_as_completed.short_description = "Mark selected bookings as completed"

# Custom action to send booking email
def send_email(modeladmin, request, queryset):
    for booking in queryset:
        booking_details = {
            'name': booking.car.name,
            'year': booking.car.year,
            'rent': booking.car.rent,
            'pickup_date': booking.pickup_date,
            'return_date': booking.return_date,
            'total_rent': booking.total_rent,
            'payment_status': booking.payment_status,
            'cus_name': booking.cus_name,  # Include customer's name
        }
        recipient_email = booking.cus_email  # Ensure this field exists
        send_booking_email(recipient_email, booking_details)  # Pass booking_details

send_email.short_description = "Send booking status email to selected users"


class BookingAdmin(admin.ModelAdmin):
    list_display = ('cus_name', 'car', 'status', 'pickup_date', 'return_date', 'total_rent')
    actions = [mark_as_completed, send_email]  # Add custom action to the admin interface


admin.site.register(Booking, BookingAdmin)

admin.site.register(Profile)
admin.site.register(Car_info)
admin.site.register(Wishlist)
