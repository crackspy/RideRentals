# Built by crackspy

from django.contrib import admin, messages
from django.template.loader import render_to_string
from .models import Profile, Car_info, Booking, Wishlist
from .utils import send_booking_email, send_booking_completed_email
# Register your models here.

# Custom action for marking booking as completed and sending email
def mark_as_completed(modeladmin, request, queryset):
    completed_count = 0
    for booking in queryset:
        if booking.status != Booking.Status.COMPLETED:

            # Prepare booking details for email
            booking_details = {
                'car_name': booking.car.name,
                'year': booking.car.year,
                'total_rent': booking.total_rent,
                'cus_name': booking.cus_name,  
            }

            # Send completion email
            recipient_email = booking.cus_email
            try:
                send_booking_completed_email(recipient_email, booking_details)
                email_status_send = True
            except:
                pass

            #Update booking status and car availability
            booking.status = Booking.Status.COMPLETED
            booking.payment_status = Booking.Payment_Status.PAID
            booking.car.available = True
            booking.car.save()
            booking.save()

            completed_count += 1

            if completed_count > 0:
                if email_status_send:
                    messages.success(request, f"{completed_count} booking completed and Email send!")
                else:
                    messages.warning(request, f"{completed_count} bookings completed and Email not!")
            else:
                messages.warning(request, "No bookings were updated!")
        else:
            messages.warning(request, "booking already completed!")

mark_as_completed.short_description = "Mark selected bookings as completed & notify customers"

# Custom action to send booking email
def send_booking_confirm_email(modeladmin, request, queryset):
    for booking in queryset:
        booking_details = {
            'name': booking.car.name,
            'year': booking.car.year,
            'rent': booking.car.rent,
            'pickup_date': booking.pickup_date,
            'return_date': booking.return_date,
            'total_rent': booking.total_rent,
            'payment_status': booking.payment_status,
            'payment_method': booking.payment_method,
            'cus_name': booking.cus_name,  # Include customer's name
        }
        recipient_email = booking.cus_email  # Ensure this field exists

        try:
            send_booking_email(recipient_email, booking_details, subject="Booking update - Ride Rentals")
            messages.success(request, f"To: {booking.cus_email} Booking update email send successfully!")
        except:
            pass

send_booking_confirm_email.short_description = "Send booking status email to selected users"


class BookingAdmin(admin.ModelAdmin):
    list_display = ('cus_name', 'car', 'status', 'pickup_date', 'return_date', 'total_rent')
    actions = [mark_as_completed, send_booking_confirm_email]  # Add custom action to the admin interface

admin.site.register(Booking, BookingAdmin)
admin.site.register(Profile)
admin.site.register(Car_info)
admin.site.register(Wishlist)
