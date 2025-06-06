# Built by crackspy

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# email sending
# send booking confirmation email
def send_booking_email(user_email, booking_details, subject="Booking Confirmation - Ride Rentals"):
    
    # Render email template
    html_message = render_to_string('mainapp/emails/booking_confirmation.html', {
        'booking_details': booking_details
    })

    # Plain text fallback message
    message = f"""
    Hello {booking_details['cus_name']},

    Your booking for {booking_details['name']} ({booking_details['year']}) has been confirmed.

    Booking Details:
    - Pick-up Date: {booking_details['pickup_date']}
    - Return Date: {booking_details['return_date']}
    - Total Rent: ₹{booking_details['total_rent']}
    
    Thank you for choosing Ride Rentals!
    """

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    # Send email
    try :
        send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
    except Exception as e:  
        print(f"Error sending booking email: {e}")

# send booking completion email
def send_booking_completed_email(user_email, booking_details):
    subject = "Your Car Rental is Completed - Thank You!"
    
    # Render email template
    html_message = render_to_string('mainapp/emails/booking_completed.html', {
        'booking_details': booking_details
    })
    
    # Plain text fallback message
    message = f"""
    Hello {booking_details['cus_name']},

    Your booking for {booking_details['car_name']} ({booking_details['year']}) has been successfully completed.

    Total Rent: ₹{booking_details['total_rent']}

    Thank you for choosing Ride Rentals!
    """

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    # Send email
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
    except Exception as e:
        print(f"Error sending booking completion email: {e}")

