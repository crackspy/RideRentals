from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import Car_info, Booking, Wishlist
from .utils import send_booking_email

from django.core.mail import send_mail
from django.http import HttpResponse
import json

# Create your views here.

# home page
def index(request):
    return render(request, 'mainapp/index.html')

#--------------------  Authentication -------------------

# login or register page
def auth_page(request):
    return render(request, 'mainapp/login/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('reg_password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password :
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
                return redirect('auth')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already taken")
                return redirect('auth')
            else:
                user_reg = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password
                )
                user_reg.save()
                return redirect('home')
        else:
            messages.error(request, "password doesnot match")
            return redirect('auth')
    else:
        return render(request, 'mainapp/login/login.html')

# login
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login Success")
            return redirect('home')
        else:
            print("error")
            messages.error(request, "User not found")
            return redirect('auth')

    return render(request, 'mainapp/login/login.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')

# -------------------------------------------------------

#-----------------------  Rental  -----------------------
@login_required
def explore_cars(request):
    featured_cars = Car_info.objects.all()  # Replace with your desired filtering logic
    return render(request, 'mainapp/rental/cars.html', {'car_list': featured_cars})

@login_required
def booking(request, slug):
    # Fetch the car details using the slug
    car = get_object_or_404(Car_info, slug=slug)
    if request.method == "POST":
        # Get logged-in user
        logged_in_user = request.user  # This gives the logged-in User instance

        # Extract form data
        cus_name = request.POST['full_name']
        cus_ph = request.POST['phone']
        cus_email = request.POST['email']
        pickup_date = request.POST['pickup_date']
        return_date = request.POST['return_date']
        notes = request.POST.get('notes', '')

        # Convert pickup_date and return_date to date objects
        pickup_date_obj = datetime.strptime(pickup_date, '%Y-%m-%d').date()
        return_date_obj = datetime.strptime(return_date, '%Y-%m-%d').date()

        # Validate dates
        if return_date_obj <= pickup_date_obj:
            raise ValueError("Return date must be after pickup date.")

        # Calculate the number of days
        days_difference = (return_date_obj - pickup_date_obj).days

        # Calculate total rent
        price_per_month = car.price
        price_per_day = price_per_month / 30  # Assuming 1 month = 30 days
        total_rent = price_per_day * days_difference

        # Create and save booking
        booking = Booking(
            cus_name=cus_name,
            cus_ph=cus_ph,
            cus_email=cus_email,
            car=car,
            cus_username=logged_in_user,
            pickup_date=pickup_date_obj,
            return_date=return_date_obj,
            notes=notes,
            price=price_per_month,
            total_rent=total_rent,
        )
        booking.save()

        booking_details = f"Car: {car.name}\nPickup Date: {pickup_date}\nReturn Date: {return_date}\nTotal Rent: {total_rent}"
        send_booking_email(cus_email, booking_details)

        # Set the car as unavailable
        car.available = False
        car.save()

        # Redirect to a success page or another appropriate page
        return redirect('success_page')

    else:
        return render(request, 'mainapp/rental/booking.html', {'car': car})

@login_required
def success_page(request):
    return render(request, 'mainapp/rental/success.html')

@login_required
def add_to_wishlist(request, slug):

    car = get_object_or_404(Car_info, slug=slug)

    # Create a new Wishlist entry for the logged-in user
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, car=car)

    if created:
        messages.success(request, "Car added to wishlist!")
    else:
        messages.warning(request, "Car is already in your wishlist.")

    return redirect('explore_cars') 

@login_required
def remove_from_wishlist(request, slug):
    car = get_object_or_404(Car_info, slug=slug)

    # Check if the wishlist entry exists for the user and car
    wishlist_item = Wishlist.objects.filter(user=request.user, car=car).first()

    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, "Car removed from wishlist!")
    else:
        messages.warning(request, "Car was not in your wishlist.")

    return redirect('profile')

@login_required
def profile_dashboard(request):
    user = request.user
    bookings = Booking.objects.filter(cus_username=user)  # Fetch bookings associated with the user
    wishlist_items = Wishlist.objects.filter(user=user)  # Fetch wishlist items

    return render(request, 'mainapp/profile.html', {
        'user': user,
        'bookings': bookings,
        'wishlist_item': wishlist_items.first(),  # Assuming only one item is shown as an example
        'all_wishlist_items': wishlist_items,
    })


# -------------------------------------------------------

def test(request):
    # Add some messages
    # messages.success(request, "Your booking was successful!")
    # messages.error(request, "Payment failed. Please try again.")
    # messages.warning(request, "Booking confirmation is pending.")

    return render(request, 'mainapp/test.html')
def test_p(request):
    # Add some messages
    # messages.success(request, "Your booking was successful!")
    # messages.error(request, "Payment failed. Please try again.")
    # messages.warning(request, "Booking confirmation is pending.")

    booking_details = {
        'rent': 45000.0,
        'pickup_date': 'Jan. 1, 2025',
        'return_date': 'Jan. 31, 2025',
        'total_rent': 45000.0,
        'payment_status': 'Pending'
    }
    
    return render(request, 'mainapp/emails/booking_confirmation.html', {
        'booking_details': booking_details
    })


def send_test_email(request):
    # subject = 'Test Email from Django'
    # message = 'This is a test email sent from your Django application.'
    # recipient_list = ['crackspy.log232@gmail.com']  # Replace with the recipient's email

    # # try:
    # #     send_mail(subject, message, 'your_email@gmail.com', recipient_list)
    # #     return HttpResponse('Test email sent successfully.')
    # # except Exception as e:
    # #     return HttpResponse(f'Error: {e}')


    # Simulate some booking details
    booking_details = {
        'rent': 45000.0,
        'pickup_date': 'Jan. 1, 2025',
        'return_date': 'Jan. 31, 2025',
        'total_rent': 45000.0,
        'payment_status': 'Pending'
    }
    
    # Send email to the user
    send_booking_email(user_email='crackspy.log232@gmail.com', booking_details=booking_details)

    return redirect('success_page')  # Redirect to a success page after booking
