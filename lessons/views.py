from django.http import HttpResponse
from django.shortcuts import render


def show_conference_view(request, room):
    return render(request, 'lessons/conference.html',
                  context={'room_name': room, 'auth': request.user.id, 'user_name': request.user.username})
