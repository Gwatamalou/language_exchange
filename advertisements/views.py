from re import search
from traceback import print_tb

from django.http import HttpResponse
from django.shortcuts import render



def advertisements_list(requests):
    return render(requests, 'advertisements/index.html')

def advertisements(request, slug_id):
    return render(request, 'advertisements/advertisement.html')
