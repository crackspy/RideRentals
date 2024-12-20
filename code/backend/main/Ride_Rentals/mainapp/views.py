from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.

# home page
def index(request):
    return render(request, 'mainapp/index.html')


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


def test(request):
    return render(request, 'mainapp/test.html')
