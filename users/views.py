from logging import exception

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import views as auth_views

from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse

from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.detail import DetailView

import logging

from advertisements.models import Notification
from language_exchange.settings import LOGIN_REDIRECT_URL, LOGIN_URL
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
    template_name = 'users/register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = register_user(form)
        if user:
            try:
                create_new_user(user)
                logger.info(f'create {user}')
                return redirect(LOGIN_URL)
            except Exception as e:
                logger.warning(e)

        return self.form_invalid(form)


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
                    messages.success(request, "Навык успешно добавлен.")
                except Exception as e:
                    logger.error(e)

            messages.error(request, "Не удалось добавить навык. Проверьте введенные данные.")

            return redirect('user-profile', user_id=self.request.user.id)


        elif "delete_skill_id" in self.request.POST:
            skill_id = request.POST.get('delete_skill_id')
            skill = get_current_language_skill(skill_id)

            if is_skill_owner(skill, request.user):
                try:
                    delete_skill(skill)
                    messages.success(request, "Навык успешно удалён.")
                except Exception as e:
                    logger.error(e)

            messages.error(request, "Вы не можете удалить этот навык.")

            return redirect('user-profile', user_id=self.request.user.id)


        elif "avatar" in self.request.FILES:
            profile = self.request.user.userprofile
            if request.FILES.get('avatar'):
                try:
                    avatar = request.FILES['avatar']
                    update_avatar(profile, avatar)
                except Exception as e:
                    logger.error(e)

            return redirect('user-profile', user_id=request.user.id)


class UpdateLanguageSkillView(LoginRequiredMixin, UpdateView):
    form_class = LanguageSkillForm
    template_name = 'users/update_language_skill.html'

    def get_object(self, queryset=None):
        skill_id = self.kwargs['skill_id']
        skill = get_current_language_skill(skill_id)
        return skill

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'instance': self.get_object(),
            'language_readonly': True,
        })
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        update_language_skill(self.request.user.id, form)
        return redirect('user-profile', user_id=self.request.user.id)


class NotificationView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'users/notification.html'
    model = Notification
    context_object_name = 'notification'

    def test_func(self):
        return True

    def handle_no_permission(self):
        pass

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
                messages.success(request, "Запрос успешно принят.")
                return redirect('lesson', room)
            except Exception as e:
                logger.error(e)
                return redirect('notification-list')

        elif 'decline' in request.POST:
            try:
                notification_delete(notification)
                messages.info(request, "Запрос отклонен.")
            except Exception as e:
                logger.error(e)
            return redirect('notification-list')


class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        """Пусть редиректа после авторизации"""
        return f'/{LOGIN_REDIRECT_URL}/{self.request.user.id}/'
