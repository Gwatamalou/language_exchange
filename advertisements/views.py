from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import error
from django.db.models import Prefetch
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView

from advertisements.froms import AdvertisementForm
from advertisements.models import Advertisement
from users.views import logger
from .services import get_current_advertisement, add_new_advertisement, \
    add_new_notification
from users.models import LanguageSkill


class AdvertisementsList(LoginRequiredMixin, ListView):
    """Представление списка объявлений"""

    template_name = 'advertisements/ads_list.html'
    model = Advertisement
    context_object_name = 'ads_with_languages'

    def get_queryset(self):
        try:
            ads = Advertisement.objects.select_related('user')
            language_skills = LanguageSkill.objects.filter(user__in=ads.values_list('user', flat=True))
            language_skills_prefetch = Prefetch('user__languageskill_set', queryset=language_skills)
            ads = ads.prefetch_related(language_skills_prefetch)


            ads_with_languages = [
                {'ads': a,
                 'language_skills': a.user.languageskill_set.all(),
                 'avatar_url': a.user.userprofile.avatar.url} for a in ads
            ]
            return ads_with_languages
        except Exception as e:
            logger.error(f'error getting ads list user {self.request.user} | {e}')
            return redirect('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'auth': self.request.user.is_authenticated,
            'user_id': self.request.user.id
        })

        return context


class SelectedAdvertisement(LoginRequiredMixin, DetailView):
    """Представление выбранного объявления"""
    template_name = 'advertisements/advertisement.html'
    model = Advertisement
    pk_url_kwarg = 'user_id'

    def get_object(self, queryset=None):
        return get_current_advertisement(self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        advertisement = self.get_object()
        avatar_url = advertisement.user.userprofile.avatar.url
        user_language_skills = LanguageSkill.objects.filter(user=advertisement.user)

        context.update({
            'auth': self.request.user.is_authenticated,
            'advertisement': advertisement,
            'avatar_url': avatar_url,
            'user_language_skills': user_language_skills,
        })

        return context

    def post(self, request, *args, **kwargs):
        """
        Обработчик пост запросов
        delete_ads: удаление своего объявления
        choose: выбор объявления и перенаправление на страницу диалога
        """

        if 'delete_ads' in request.POST:
            ads_id = request.POST.get('delete_ads')
            ads = get_object_or_404(Advertisement, id=ads_id)
            try:
                if ads.user == request.user:
                    ads.delete()
                    logger.info(f'delete ads {ads_id} user {self.request.user}')
                else:
                    logger.warning(f'user {self.request.user} attempt to delete someone`s ads')
            except Exception as e:
                logger.error(f'error delete ads {ads_id} | {e}')

            return redirect('ads_list')

        elif 'choose' in request.POST:
            ads_id = request.POST.get('choose')
            ads = Advertisement.objects.get(id=ads_id)
            try:
                add_new_notification(request.user, ads)
                room = f'{request.user}{ads.user.username}'
                return redirect('lesson', room)
            except Exception as e:
                logger.error(f'failed to create dialogue room user {self.request.user} | {e}')

            return redirect('ads_list')



class MakeAdvertisement(LoginRequiredMixin, FormView):
    """Представление формы создания объявления"""
    template_name = 'advertisements/add_ads.html'
    form_class = AdvertisementForm

    def form_valid(self, form):
        try:
            add_new_advertisement(self.request.user, form)
        except Exception as e:
            logger.error(f'failed to create new ads user {self.request.user} | {e}')
        return redirect('ads_list')
