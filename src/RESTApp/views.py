# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hi there, this is in the REST API route!")
