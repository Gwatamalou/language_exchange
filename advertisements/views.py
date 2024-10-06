from re import search
from traceback import print_tb

from django.http import HttpResponse
from django.shortcuts import render



def show_advertisements_list(requests):
    return render(requests, 'advertisements/ads_list.html')


def show_selected_advertisement_view(request, slug_id):
    return render(request, 'advertisements/advertisement.html')
