from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# return text to html

def index_page(request):
    return render(request, 'index.html')


def print_hello(request):
    return HttpResponse("hello")

# return html page
def hello_page(request):
    return render(request, 'hello.html')

# pass variables
def one_page(request):
    movie_details = {
        'movies': [
            {
            'title': 'god Father',
            'year': '1990',
            'summary': 'Story of a underworld king',
            'success': True
        },
        {
            'title': 'Titanic',
            'year': '2002',
            'summary': '',
            'success': True
        },
        {
            'title': 'on2',
            'year': '1990',
            'summary': 'Story of a underworld king',
            'success': True
        },
        {
            'title': 'Gon4',
            'year': '1990',
            'summary': 'Story',
            'success': False
        }
    ]}
    
    #pass variable as dict
    return render(request, 'one.html', movie_details)











