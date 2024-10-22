from django.http import HttpResponse
from django.shortcuts import render


def show_conference_view(request):
    return render(request, 'lessons/conference.html',
                  context={'room_name': 'lesson', 'auth': request.user.id})
