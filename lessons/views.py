from django.http import HttpResponse
from django.shortcuts import render

def show_user_lesson_view(requests):
    return render(requests, 'lessons/lessons_list.html', context={'title': 'lesson'})

def show_conference_view(requests):
    return render(requests, 'lessons/conference.html')