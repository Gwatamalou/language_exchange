from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from constants import LANGUAGE_LIST, LEVEL_SKILL
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from .forms import LanguageSkillForm

from users.models import LanguageSkill

# Qwertyui1.
def index(request):
    """Начальная страницы"""
    return render(request, 'base.html')


@login_required
def show_user_profile_view(request, user_id):
    """Отображение профиля пользователя"""

    user = get_user(user_id)
    user_language = get_user_language(user.id)

    if user != request.user:
        return redirect('login')

    form = LanguageSkillForm()
    data = {
        'title': 'User',
        'language': LANGUAGE_LIST,
        'level': LEVEL_SKILL,
        'auth': request.user.is_authenticated,
        'user': user,
        'user_language': user_language,
        'form': form,
    }
    return render(request, 'users/user_profile.html', context=data)


@login_required
def add_new_language(request):
    """Добавление информации о знании языка"""
    if request.method == 'POST':
        form = LanguageSkillForm(request.POST)
        if form.is_valid():
            language_skill = form.save(commit=False)
            language_skill.user = request.user
            language_skill.save()
            return redirect('user_profile', user_id=request.user.id)


@login_required
def update_language_skill_view(request, skill_id):
    """Обновление уровня языкового навыка"""
    skill = get_object_or_404(LanguageSkill, id=skill_id)

    if skill.user != request.user:
        return redirect('login')

    if request.method == 'POST':
        form = LanguageSkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id=request.user.id)
    else:
        form = LanguageSkillForm(instance=skill)

    data = {
        'form': form,
        'skill': skill,
    }
    return render(request, 'users/update_language_skill.html', context=data)


@login_required
def delete_language_skill_view(request, skill_id):
    """удаление информации о знании языка"""
    skill = get_object_or_404(LanguageSkill, id=skill_id)

    if skill.user == request.user:
        skill.delete()
        return redirect('user_profile', user_id=request.user.id)
    else:
        return redirect('login')


class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        """Пусть редиректа после авторизации"""
        return f'/profile/{self.request.user.id}/'


def get_user(user_id):
    """Получение данных о пользователе из бд"""
    return get_object_or_404(User, id=user_id)


def get_user_language(user_id):
    """Получение данных о языках и уровнях владения из бд"""
    return LanguageSkill.objects.filter(user_id=user_id)
