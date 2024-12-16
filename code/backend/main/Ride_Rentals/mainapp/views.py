from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'mainapp/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

    
    return render(request, 'mainapp/login/login.html')
