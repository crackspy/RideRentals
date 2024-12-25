from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages

from . models import Car_info, Booking

# Create your views here.

# home page
def index(request):
    return render(request, 'mainapp/index.html')

def index_home(request):
    return render(request, 'mainapp/home/index.html')

def explore_cars(request):
    featured_cars = Car_info.objects.all()  # Replace with your desired filtering logic
    return render(request, 'mainapp/home/cars.html', {'car_list': featured_cars})


def car_detail(request, slug):
    car = get_object_or_404(Car_info, slug=slug) 
    return render(request, 'mainapp/home/car_detail.html', {'car': car}) 

#---------------------  Authentication ----------------

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
        print(user)
        if user is not None:
            auth.login(request, user)
            messages.info(request, "Login Success")
            return redirect('test')
        else:
            print("error")
            messages.info(request, "User not found")
            return redirect('auth')

    return render(request, 'mainapp/login/login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

# -------------------------------------------------------

def test(request):
    return render(request, 'mainapp/test.html')
