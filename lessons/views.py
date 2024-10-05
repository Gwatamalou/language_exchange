from django.http import HttpResponse
from django.shortcuts import render

def lesson(requests):
    return render(requests, 'lessons/index.html', context={'title': 'lesson'})

def conference(requests):
    return render(requests, 'lessons/conference.html')