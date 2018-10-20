# Create your views here.
from django.http import HttpResponse


def index(request):
    print(request)
    response = "Nice request you got there: %s" % request
    return HttpResponse(response)
