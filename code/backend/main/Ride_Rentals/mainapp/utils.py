from django.core.mail import send_mail
from django.conf import settings

def send_booking_email(user_email, booking_details):
    subject = "Booking Confirmation"
    message = f"Thank you for booking with us! Here are your booking details:\n\n{booking_details}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
    
