from django.contrib import admin
from .models import Car_info, Booking, Wishlist
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

class BookingAdmin(admin.ModelAdmin):
    list_display = ('cus_name', 'car', 'status', 'pickup_date', 'return_date', 'total_rent')
    actions = [mark_as_completed]  # Add custom action to the admin interface

admin.site.register(Booking, BookingAdmin)


admin.site.register(Car_info)
# admin.site.register(Booking)
admin.site.register(Wishlist)
