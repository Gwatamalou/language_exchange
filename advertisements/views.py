from django.http import HttpResponse
from django.shortcuts import render

def advertisements(requests):
    return render(requests, 'advertisements/index.html')