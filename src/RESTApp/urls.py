from django.conf.urls import url

from RESTApp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
