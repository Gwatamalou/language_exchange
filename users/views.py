from django.db.models.fields import return_None
from django.http import HttpResponse
from django.shortcuts import render
from constants import LANGUAGE_LIST, LEVEL_SKILL, MENU
from users.models import UserProfile
from django.contrib.auth.models import User

# Qwertyui1.




def show_user_profile_view(requests):
    user = User.objects.filter(username='Adam')
    data = {
        'title': 'User',
        'language': LANGUAGE_LIST,
        'level': LEVEL_SKILL,
        'menu': MENU,
        'user': user
    }
    return render(requests, 'users/user_profile.html', context=data)

