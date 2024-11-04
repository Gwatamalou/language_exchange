from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import views as auth_views

from advertisements.models import Notification
from language_exchange.settings import LOGIN_REDIRECT_URL, LOGIN_URL
from constants import LANGUAGE_LIST, LEVEL_SKILL
from .forms import LanguageSkillForm
from .models import UserProfile
from .services import *


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
            create_new_user(user)
            messages.success(self.request, "Регистрация прошла успешно. Войдите в свой аккаунт.")
            return redirect(LOGIN_URL)
        else:
            messages.error(self.request, "Ошибка при регистрации. Пожалуйста, попробуйте снова.")
            form = UserCreationForm()
            return render(self.request, self.template_name, {'form': form})



class UserProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'users/user_profile.html'
    model = UserProfile

    def get_object(self, queryset=None):
        """Переопределяем get_object для получения UserProfile по user_id"""
        user_id = self.kwargs['user_id']
        return get_object_or_404(UserProfile, user_id=user_id)

    def test_func(self):
        """Проверка, что пользователь просматривает свой профиль"""
        user_id = int(self.kwargs['user_id'])
        return self.request.user.id == user_id

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет доступа к этому профилю.")
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
                add_language_skill(self.request.user, form)
                messages.success(request, "Навык успешно добавлен.")
            else:
                messages.error(request, "Не удалось добавить навык. Проверьте введенные данные.")

            return redirect('user-profile', user_id=self.request.user.id)


        elif "delete_skill_id" in self.request.POST:
            skill_id = request.POST.get('delete_skill_id')
            skill = get_current_language_skill(skill_id)

            if is_skill_owner(skill, request.user):
                delete_skill(skill)
                messages.success(request, "Навык успешно удалён.")
            else:
                messages.error(request, "Вы не можете удалить этот навык.")

            return redirect('user-profile', user_id=self.request.user.id)

        # elif "avatar" in self.request.POST:
        else:
            profile = self.request.user.userprofile
            if request.FILES.get('avatar'):
                    avatar = request.FILES['avatar']
                    update_avatar(profile, avatar)

            return redirect('user-profile', user_id=request.user.id)


class UpdateLanguageSkillView(LoginRequiredMixin, UpdateView):
    form_class = LanguageSkillForm
    template_name = 'users/update_language_skill.html'

    def get_object(self, queryset=None):
        skill_id = self.kwargs['skill_id']
        skill = get_current_language_skill(skill_id)
        return skill

    def form_valid(self, form):
        form.instance.user = self.request.user
#       form = LanguageSkillForm(request.POST, instance=skill, language_readonly=True)
        update_language_skill(self.request.user.id, form)
        return redirect('user-profile', user_id=self.request.user.id)



class NotificationView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'users/notification.html'
    model = Notification

    def test_func(self):
        return True

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет доступа к этому профилю.")
        print(12)
        return redirect(LOGIN_URL)

    def get_object(self, queryset=None):
        notification = get_notification(self.request.user.id)
        return notification

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notification = self.get_object()
        context.update({
            'auth': self.request.user.is_authenticated,
            'notification': notification,
        })

        return context

    def post(self, request, *args, **kwargs):

        notification_id = request.POST.get("accept") or request.POST.get("decline")
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
