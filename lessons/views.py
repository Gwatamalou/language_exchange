from django.http import HttpResponse
from django.shortcuts import render


def show_conference_view(request):
    return render(request, 'lessons/lessons_list.html',
                  context={'title': 'lesson', 'auth': request.user.id})
