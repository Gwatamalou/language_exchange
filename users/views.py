from django.http import HttpResponse
from django.shortcuts import render
from constants import LENGTH_LIST, LEVEL_SKILL, MENU

def user_profile(requests):
    data = {
        'title': 'User',
        'length': LENGTH_LIST,
        'level': LEVEL_SKILL,
        'menu': MENU,

    }
    return render(requests, 'users/index.html', context=data)
