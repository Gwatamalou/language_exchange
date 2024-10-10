from lib2to3.fixes.fix_input import context
from pickletools import uint1

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from advertisements.froms import AdvertisementForm
from advertisements.models import Advertisement, Notification


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
    advertisement = Advertisement.objects.filter(id=slug_id).first()
     
    data = {
        'ads': ads,
        'auth': request.user.is_authenticated,
        'advertisement': advertisement
    }
    return render(request, 'advertisements/advertisement.html',
                  context=data)


@login_required
def show_make_advertisement_view(request):
    """страница создание нового объявления"""
    form = AdvertisementForm()
    data = {
        'form': form,
        'auth': request.user.is_authenticated,
    }
    return render(request, 'advertisements/add_ads.html', context=data)


def add_advertisement(request):
    """добавление нового объявления в бд"""
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()
            return redirect('ads_list')


@login_required
def choose_advertisement_view(request, slug_id):
    """Обработка выбора объявления"""
    """отображение страницы уведомлений"""
    advertisement = Advertisement.objects.get(id=slug_id)
    if advertisement.user == request.user:
        notificat = Notification.objects.filter(user_id=request.user.id)
        data = {
            'auth': request.user.is_authenticated,
            'notificat': notificat,
        }
        return render(request, 'advertisements/notification.html',
                      context=data)

    """обработка выбора"""
    Notification.objects.create(
        responder=request.user,
        user=advertisement.user,
        advertisement=advertisement,
        status='pending',
    )

    return redirect('lesson')

@login_required
def notification(request, notification_id):
    """Страница отклика на уведомление с кнопками принять/отклонить"""
    notification = Notification.objects.get(id=notification_id, user=request.user)

    if request.method == 'POST':
        if 'accept' in request.POST:
            # Обработка принятия отклика
            notification.status = 'accepted'
            notification.save()
            # Здесь можно добавить логику для перенаправления на видео-чат
            return redirect('lesson')  # Или другая нужная страница
        elif 'decline' in request.POST:
            # Обработка отклонения отклика
            notification.status = 'declined'
            notification.save()
            # Сообщаем пользователю, что его предложение отклонено
            return redirect('ads_list')  # Перенаправление на страницу с объявлениями
