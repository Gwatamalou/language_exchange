from pickletools import uint1

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from advertisements.froms import AdvertisementForm
from advertisements.models import Advertisement


def show_advertisements_list(request):
    """список объявление """
    ads = Advertisement.objects.all()
    data = {
        'ads': ads,
        'auth': request.user.is_authenticated,
    }
    return render(request, 'advertisements/ads_list.html', context=data)


@login_required
def show_selected_advertisement_view(request, slug_id):
    """страница отображения выборного объявления и списка других объявлений пользователя"""
    ads = Advertisement.objects.filter(user_id=request.user.id)
     
    data = {
        'ads': ads,
        'auth': request.user.is_authenticated,
    }
    return render(request, 'advertisements/advertisement.html',
                  context=data)


@login_required
def show_make_advertisement_view(request):
    form = AdvertisementForm()
    data = {
        'form': form,
        'auth': request.user.is_authenticated,
    }
    return render(request, 'advertisements/add_ads.html', context=data)


def add_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()
            return redirect('ads_list')
