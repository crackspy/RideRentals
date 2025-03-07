from django.shortcuts import render
from django.http import HttpResponse
from . models import MovieInfo

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


# return static files
def show_image(request):
    return render(request, 'image.html')

def crud(request):
    return render(request, 'crud/crud.html')

def crud_list(request):
    movie_set = MovieInfo.objects.all()
    return render(request, 'crud/list.html', {'movies': movie_set})

# get data from frontend
def crud_create(request):
    if request.POST:
        # print(request.POST)
        # print(request.POST.get('title'))
        # print(request.POST.get('year'))

        title =  request.POST.get('title')
        year = request.POST.get('year')
        summary = request.POST.get('summary')

        Movie_obj = MovieInfo(title=title, year=year, summary=summary)
        Movie_obj.save()


    return render(request, 'crud/create.html')

def crud_delete(request):
    return render(request, 'crud/delete.html')

def crud_modify(request):
    return render(request, 'crud/modify.html')

def crud_update(request):
    return render(request, 'crud/update.html')



