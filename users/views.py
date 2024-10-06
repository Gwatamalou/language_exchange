from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from constants import LANGUAGE_LIST, LEVEL_SKILL
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
# Qwertyui1.


def index(request):
    return render(request, 'base.html')

@login_required
def show_user_profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        return redirect('login')
    data = {
        'title': 'User',
        'language': LANGUAGE_LIST,
        'level': LEVEL_SKILL,
        'user': user,
    }
    return render(request, 'users/user_profile.html', context=data)

class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        return f'/profile/{self.request.user.id}/'
