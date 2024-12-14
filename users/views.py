from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth import views as auth_views

from django.shortcuts import render, redirect, reverse


from django.views.generic import ListView
from django.views.generic.edit import FormView
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
        user_id = self.kwargs['user_id']
        return get_user_data(user_id)

    def test_func(self):
        return self.request.user.id == int(self.kwargs['user_id'])

    def handle_no_permission(self):
        return redirect(LOGIN_URL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user, user_language, avatar_url = get_all_user_data(user_id=self.kwargs['user_id'])
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

        if 'add_skill' in self.request.POST:
            form = LanguageSkillForm(request.POST)
            add_language_skill(self.request.user, form)


        elif 'update_skill' in self.request.POST:
            skill_id = request.POST.get('skill_id')
            skill = get_current_language_skill(skill_id)

            if is_skill_owner(skill, request.user):
                form = LanguageSkillForm(request.POST, instance=skill)
                update_language_skill(self.request.user.id, form)


        elif "delete_skill_id" in self.request.POST:
            skill_id = request.POST.get('delete_skill_id')
            skill = get_current_language_skill(skill_id)

            if is_skill_owner(skill, request.user):
                    delete_skill(self.request.user, skill)


        elif "avatar" in self.request.FILES:
            profile = self.request.user.userprofile
            if request.FILES.get('avatar'):
                avatar = request.FILES['avatar']
                update_avatar(profile, avatar)
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
            room = notification_accept(notification)
            if room:
                return redirect('lesson', room)


        elif 'decline' in request.POST:
                notification_delete(notification)

class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        """Пусть редиректа после авторизации"""
        return reverse('user-profile', args=(self.request.user.id, ))


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        """Редирект после успешной смены пароля"""
        return reverse('user-profile', args=(self.request.user.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'auth': self.request.user.is_authenticated,
        })

        return context