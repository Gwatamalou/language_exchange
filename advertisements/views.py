from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Case, When, IntegerField
from django.db.models.sql.query import get_order_dir
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from advertisements.froms import AdvertisementForm
from advertisements.models import Advertisement
from users.views import logger
from .services import *
from .services.advertisement_services import delete_ads, choose_ads


class AdvertisementsList(LoginRequiredMixin, ListView):
    template_name = 'advertisements/ads_list.html'
    model = Advertisement
    context_object_name = 'ads_with_languages'

    def get_queryset(self):
            ads = get_ads(self.request.user.id, self.kwargs.get('slug'))

            language_skills = get_order_language_skill(ads)

            language_skills_prefetch = Prefetch('user__languageskill_set', queryset=language_skills)
            ads = ads.prefetch_related(language_skills_prefetch)

            ads_with_languages = [
                {'ads': a,
                 'language_skills': a.user.languageskill_set.all(),
                 'avatar_url': a.user.userprofile.avatar.url} for a in ads
            ]

            return ads_with_languages


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'auth': self.request.user.is_authenticated,
            'user_id': self.request.user.id
        })

        return context


class SelectedAdvertisement(LoginRequiredMixin, DetailView):
    template_name = 'advertisements/advertisement.html'
    model = Advertisement
    pk_url_kwarg = 'user_id'

    def get_object(self, queryset=None):
        return get_current_advertisement(self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        advertisement = self.get_object()
        avatar_url = get_avatar_url(advertisement)
        user_language_skills = get_user_language_skills(advertisement)

        context.update({
            'auth': self.request.user.is_authenticated,
            'advertisement': advertisement,
            'avatar_url': avatar_url,
            'user_language_skills': user_language_skills,
        })

        return context

    def post(self, request, *args, **kwargs):

        if 'delete_ads' in request.POST:
            ads_id = request.POST.get('delete_ads')
            delete_ads(request.user, ads_id)
            return redirect('ads_list', 'my')

        elif 'choose' in request.POST:
            ads_id = request.POST.get('choose')
            room = choose_ads(request.user, ads_id)

            if room:
                return redirect('lesson', room)

            return redirect('ads_list', 'all')


class MakeAdvertisement(LoginRequiredMixin, FormView):
    template_name = 'advertisements/add_ads.html'
    form_class = AdvertisementForm

    def form_valid(self, form):

        add_new_advertisement(self.request.user, form)
        return redirect('ads_list', 'my')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'auth': self.request.user.is_authenticated,
        })

        return context