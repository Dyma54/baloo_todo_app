from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, template_name='todo_site/home.html')