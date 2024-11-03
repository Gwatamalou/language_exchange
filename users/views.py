from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from advertisements.models import Notification
from constants import LANGUAGE_LIST, LEVEL_SKILL

from django.contrib.auth import views as auth_views
from language_exchange.settings import LOGIN_REDIRECT_URL, LOGIN_URL
from .forms import LanguageSkillForm, AvatarForm
from .models import UserProfile

# from .services import (register_user, get_user_data, add_language_skill, get_current_language, update_language_skill,
#                        check_skill_owner, get_notification)

from .services import *
from .services.services import delete_skill, update_avatar, notification_accept, notification_delete, \
    get_current_notification


# Qwertyui1.
def index(request):
    """Начальная страницы"""
    return render(request, 'base.html', {'auth': request.user.is_authenticated})


def register(request):
    """страница регистрации"""
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        user = register_user(form)
        if user:
            create_new_user(user)
            return redirect(LOGIN_URL)
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})




@login_required
def show_user_profile_view(request, user_id):
    """Отображение профиля пользователя"""
    user, user_language, avatar_url = get_user_data(user_id=user_id)

    if user != request.user:
        return redirect(LOGIN_URL)


    form = LanguageSkillForm()
    data = {
        'title': 'User',
        'language': LANGUAGE_LIST,
        'level': LEVEL_SKILL,
        'auth': request.user.is_authenticated,
        'user': user,
        'user_language': user_language,
        'form': form,
        'avatar_url': avatar_url,
    }
    return render(request, 'users/user_profile.html', context=data)


@login_required
def create_language_handler(request):
    """Добавление информации о знании языка"""
    if request.method == 'POST':
        form = LanguageSkillForm(request.POST)
        add_language_skill(request.user, form)
    return redirect('user-profile', user_id=request.user.id)


@login_required
def update_language_skill_handler(request, skill_id):
    """Обновление уровня языкового навыка"""
    skill = get_current_language(skill_id)

    if not check_skill_owner(skill, request.user):
        return redirect(LOGIN_URL)

    if request.method == 'POST':
        form = LanguageSkillForm(request.POST, instance=skill, language_readonly=True)
        update_language_skill(request.user.id, form)
        return redirect('user-profile', user_id=request.user.id)
    else:
        form = LanguageSkillForm(instance=skill, language_readonly=True)

    data = {
        'form': form,
        'skill': skill,
        'auth': request.user.is_authenticated,
    }

    return render(request, 'users/update_language_skill.html', context=data)


@login_required
def delete_language_skill_handler(request, skill_id):
    """удаление информации о знании языка"""
    skill = get_current_language(skill_id)

    if check_skill_owner(skill, request.user):
        delete_skill(skill)
        return redirect('user-profile', user_id=request.user.id)
    else:
        return redirect(LOGIN_URL)

@login_required
def update_avatar_handler(request):
    if request.method == 'POST':
        profile = request.user.userprofile

        if request.FILES.get('avatar'):
            avatar = request.FILES['avatar']
            update_avatar(profile, avatar)

    return redirect('user-profile', user_id=request.user.id)

@login_required
def show_notification_view(request):
    """Отображение страницы уведомлений"""
    notification = get_notification(request.user.id)

    data = {
        'auth': request.user.is_authenticated,
        'notificat': notification,
    }
    return render(request, 'users/notification.html', context=data)



@login_required
def notification_response_handler(request, notification_id):
    """Обработчик отклика на уведомление принять/отклонить"""
    notification = get_current_notification(notification_id, request.user)

    if request.method == 'POST':
        if 'accept' in request.POST:
            room = notification_accept(notification)
            return redirect('lesson', room)

        elif 'decline' in request.POST:
            notification_delete(notification)
            return redirect('notification-list')

class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        """Пусть редиректа после авторизации"""
        return f'/{LOGIN_REDIRECT_URL}/{self.request.user.id}/'

