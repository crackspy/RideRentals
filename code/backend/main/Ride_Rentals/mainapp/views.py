from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import Car_info, Booking, Wishlist
from .utils import send_booking_email

from django.core.mail import send_mail
from django.http import HttpResponse

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
                messages.info(request, "Username already taken")
                return redirect('auth')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
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
            messages.info(request, 'password doesnot match')
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
            messages.info(request, "Login Success")
            return redirect('home')
        else:
            print("error")
            messages.info(request, "User not found")
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
    # Fetch the car object by its slug
    car = get_object_or_404(Car_info, slug=slug)

    # Create a new Wishlist entry for the logged-in user
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, car=car)

    if created:
        message = "Car added to wishlist!"
    else:
        message = "Car is already in your wishlist."

    # Optionally, redirect to the user's wishlist page or show a success message
    return redirect('home')  # Redirect to the wishlist view or use a message

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
    return render(request, 'mainapp/profile.html')

def send_test_email(request):
    subject = 'Test Email from Django'
    message = 'This is a test email sent from your Django application.'
    recipient_list = ['crackspy.log232@gmail.com']  # Replace with the recipient's email

    try:
        send_mail(subject, message, 'your_email@gmail.com', recipient_list)
        return HttpResponse('Test email sent successfully.')
    except Exception as e:
        return HttpResponse(f'Error: {e}')
