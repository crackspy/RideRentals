# Built by crackspy

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.db import transaction
from django.utils.http import url_has_allowed_host_and_scheme
from datetime import datetime

from .models import Profile, Car_info, Booking, Wishlist
from .utils import send_booking_email
from .forms import ProfileUpdateForm

# home page
def index(request):
    featured_cars = Car_info.objects.filter(available=True)[:6]
    return render(request, 'mainapp/index.html', {'car_list': featured_cars})

#------------------------------------
#          Authentication
#------------------------------------

# login or register page
def auth_page(request):
    return render(request, 'mainapp/login/login.html')

# register user
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('reg_password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('auth')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another.")
            return redirect('auth')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('auth')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('auth')

    return render(request, 'mainapp/login/login.html')


# login
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', 'home')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            
            # Redirect to the next URL if safe
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('home')

        messages.error(request, "Invalid username or password. Please try again.")
        return redirect('auth')

    return render(request, 'mainapp/login/login.html', {'next': request.GET.get('next', '')})

# logout
@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')

# password-reset-view
class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        # Check if the email exists in the database
        email = form.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "The email address does not exist in our records.")
            return redirect('password_reset')  # Redirect to the same page
        return super().form_valid(form)


#------------------------------------
#               Rental
#------------------------------------

# cars page
@login_required
def explore_cars(request):
    featured_cars = Car_info.objects.all()
    return render(request, 'mainapp/rental/cars.html', {'car_list': featured_cars})

# booking
@login_required
def booking(request, slug):
    car = get_object_or_404(Car_info, slug=slug)
    user = request.user
    today_date = datetime.now().strftime('%Y-%m-%d')

    if request.method == "POST":

        pickup_date = request.POST['pickup_date']
        return_date = request.POST['return_date']

        # Convert pickup_date and return_date to date objects
        pickup_date_obj = datetime.strptime(pickup_date, '%Y-%m-%d').date()
        return_date_obj = datetime.strptime(return_date, '%Y-%m-%d').date()

        # Validate dates
        if return_date_obj <= pickup_date_obj:
            raise ValueError("Return date must be after pickup date.")

        # Calculate the number of days
        days_difference = (return_date_obj - pickup_date_obj).days

            # Calculate total rent
        price_per_month = car.rent
        price_per_day = price_per_month / 30  # Assuming 1 month = 30 days
        total_rent = round(price_per_day * days_difference)

        # Store booking details in session
        request.session['booking_data'] = {
            'cus_name': request.POST['full_name'],
            'cus_ph': request.POST['phone'],
            'cus_email': request.POST['email'],
            'pickup_date': pickup_date,
            'return_date': return_date,
            'total_rent': total_rent,
            'car_id': car.id
        }

        return redirect('confirm_booking', slug=car.slug) # Redirect to payment page

    return render(request, 'mainapp/rental/booking.html', {'car': car, 'today_date': today_date, 'user': user})

# confim or payment selection
@login_required
def confirm_booking(request, slug):
    car = get_object_or_404(Car_info, slug=slug)
    user = request.user

    # Retrieve booking details from session
    booking_data = request.session.get('booking_data')

    if not car.available:
        messages.error(request, "Car is not available for booking.")
        return redirect('explore_cars')

    if not booking_data:
        messages.error(request, "Session expired. Please rebook.")
        return redirect('booking', slug=slug)

    # Ensure 'total_rent' exists
    total_rent = booking_data.get('total_rent')
    if total_rent is None:
        messages.error(request, "Booking details are incomplete. Please re-enter your details.")
        return redirect('booking', slug=slug)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return render(request, 'mainapp/payment/confirm_booking.html', {'car': car, 'total_amount': total_rent})

        # Create and save the booking
        booking = Booking(
            cus_name=booking_data['cus_name'],
            cus_ph=booking_data['cus_ph'],
            cus_email=booking_data['cus_email'],
            car=car,
            cus_username=user,
            pickup_date=datetime.strptime(booking_data['pickup_date'], '%Y-%m-%d').date(),
            return_date=datetime.strptime(booking_data['return_date'], '%Y-%m-%d').date(),
            rent=car.rent,
            total_rent=total_rent,
            payment_method=payment_method,
            payment_status="Pending" if payment_method == "Cash on Delivery" else "Paid",
        )

        booking.save()
        car.available = False  # Mark car as unavailable
        car.save()

        # Send confirmation email
        booking_details = {
            'name': car.name,
            'year': car.year,
            'rent': car.rent,
            'pickup_date': booking.pickup_date,
            'return_date': booking.return_date,
            'total_rent': booking.total_rent,
            'payment_status': booking.payment_status,
            'cus_name': booking.cus_name,
        }

        send_booking_email(booking.cus_email, booking_details)

        # Clear session data after successful booking
        del request.session['booking_data']

        return redirect('success_page')  # Redirect to a success page

    return render(request, 'mainapp/payment/confirm_booking.html', {'car': car, 'total_amount': total_rent})

# payment success
@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Mark payment as complete
    booking.payment_status = "Completed"
    booking.save()

    messages.success(request, "Payment successful! Your booking is confirmed.")
    return redirect('success_page')

@login_required
def success_page(request):
    return render(request, 'mainapp/rental/success.html')

# Handle wishlist
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

#  profile page
@login_required
def profile_dashboard(request):
    user = request.user
    try:
        user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        # Redirect to a profile creation page or create a new profile automatically
        user_profile = Profile.objects.create(user=user)
    bookings = Booking.objects.filter(cus_username=user).order_by('-id') # Fetch bookings associated with the user
    wishlist_items = Wishlist.objects.filter(user=user).order_by('-id')  # Fetch wishlist items

    return render(request, 'mainapp/profile/profile.html', {
        'user': user,
        'user_profile': user_profile,
        'all_bookings': bookings,
        'booking_item': bookings.first(),
        'wishlist_item': wishlist_items.first(),
        'all_wishlist_items': wishlist_items,
    })

# update profile
@login_required
def update_profile(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, user=user)

        if form.is_valid():
            form.save(user)

            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")

    else:
        form = ProfileUpdateForm(user=user, initial={
            "phone_number": profile.phone_number,
            "profile_picture": profile.profile_picture,
        })

    return render(request, "mainapp/profile/update_profile.html", {"form": form, "user_profile": profile})

#------------------------------------
#        custom  admin views
#------------------------------------

# Function to check if the user is an admin
def admin_required(user):
    return user.is_superuser

@user_passes_test(admin_required)
def admin_only_view(request):
    return redirect('profile')
