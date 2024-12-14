from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth import views as auth_views

from django.shortcuts import render, redirect, get_object_or_404, reverse


from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.detail import DetailView

import logging

from advertisements.models import Notification
from language_exchange.settings import LOGIN_URL
from constants import LANGUAGE_LIST, LEVEL_SKILL
from .forms import LanguageSkillForm
from .models import UserProfile
from .services import *


logger = logging.getLogger(__name__)

# Qwertyui1.
def index(request):
    """Начальная страницы"""
    return render(request, 'base.html', {'auth': request.user.is_authenticated})


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        return redirect(LOGIN_URL) if register_user(form, self.request.user) else self.form_invalid(form)


class UserProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'users/user_profile.html'
    model = UserProfile

    def get_object(self, queryset=None):
        """Переопределяем get_object для получения UserProfile по user_id"""
        user_id = self.kwargs['user_id']
        return get_object_or_404(UserProfile, user_id=user_id)

    def test_func(self):
        """Проверка, что пользователь просматривает свой профиль"""
        return self.request.user.id == int(self.kwargs['user_id'])

    def handle_no_permission(self):
        return redirect(LOGIN_URL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user, user_language, avatar_url = get_user_data(user_id=self.kwargs['user_id'])
        context.update({
            'title': 'User',
            'language': LANGUAGE_LIST,
            'level': LEVEL_SKILL,
            'auth': self.request.user.is_authenticated,
            'user': user,
            'user_language': user_language,
            'form': LanguageSkillForm(),
            'avatar_url': avatar_url,
        })

        return context

    def post(self, request, *args, **kwargs):
        """Обработка отправленной формы для добавления языкового навыка"""
        if 'add_skill' in self.request.POST:
            form = LanguageSkillForm(request.POST)
            if form.is_valid():
                try:
                    add_language_skill(self.request.user, form)
                    logger.info(f'added is user skill {self.request.user}')
                except Exception as e:
                    logger.error(f'error adding user skill {self.request.user} | {e}')
            else:
                logger.warning(f'skill addition form is invalid for the user {self.request.user}')


        elif 'update_skill' in self.request.POST:
            skill_id = request.POST.get('skill_id')
            skill = get_current_language_skill(skill_id)

            if is_skill_owner(skill, request.user):
                form = LanguageSkillForm(request.POST, instance=skill)
                if form.is_valid():
                    try:
                        update_language_skill(self.request.user.id, form)
                        logger.info(f'skill updated for user {self.request.user}')
                    except Exception as e:
                        logger.error(f'error updating skill for user {self.request.user} | {e}')
                else:
                    logger.warning(f'skill update form is invalid for user {self.request.user}')
            else:
                logger.warning(f'user {self.request.user} attempted to update someone else\'s skill')



        elif "delete_skill_id" in self.request.POST:
            skill_id = request.POST.get('delete_skill_id')
            skill = get_current_language_skill(skill_id)

            if is_skill_owner(skill, request.user):
                try:
                    delete_skill(skill)
                    logger.info(f' skill has been deleted for the user {self.request.user}')
                except Exception as e:
                    logger.error(f'Error when deleting a skill for a user {self.request.user} | {e}')
            else:
                logger.warning(f'user {self.request.user} attempt to delete someone`s skill')




        elif "avatar" in self.request.FILES:
            profile = self.request.user.userprofile
            if request.FILES.get('avatar'):
                try:
                    avatar = request.FILES['avatar']
                    update_avatar(profile, avatar)
                    logger.info(f'add new avatar for {self.request.user}')
                except Exception as e:
                    logger.error(f'error add new avatar for user {self.request.user} | {e}')

        return redirect('user-profile', user_id=self.request.user.id)


class NotificationView(LoginRequiredMixin, ListView):
    template_name = 'users/notification.html'
    model = Notification
    context_object_name = 'notification'


    def get_queryset(self):
        return get_notification(self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'auth': self.request.user.is_authenticated,
        })

        return context

    def post(self, request, *args, **kwargs):

        notification_id = request.POST.get("accept") or request.POST.get("decline")
        notification = get_current_notification(notification_id, request.user)

        if 'accept' in request.POST:
            try:
                room = notification_accept(notification)
                logger.info(f'notification {notification_id} accept {self.request.user}')
                return redirect('lesson', room)
            except Exception as e:
                logger.error(f'failed accept notification {notification_id} user {self.request.user} | {e}')
                return redirect('notification-list')

        elif 'decline' in request.POST:
            try:
                notification_delete(notification)
                logger.info(f'notification {notification_id} decline {self.request.user}')
            except Exception as e:
                logger.error(f'failed decline notification {notification_id} user {self.request.user} | {e}')
            return redirect('notification-list')


class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        """Пусть редиректа после авторизации"""
        return reverse('user-profile', args=(self.request.user.id, ))


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        """Редирект после успешной смены пароля"""
        return reverse('user-profile', args=(self.request.user.id,))

    def get_context_data(self, **kwargs):
        """Добавить дополнительные данные в контекст"""
        context = super().get_context_data(**kwargs)
        context.update({
            'auth': self.request.user.is_authenticated,
        })

        return context