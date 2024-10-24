from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from advertisements.froms import AdvertisementForm
from advertisements.models import Advertisement, Notification
from advertisements.services import get_advertisement_user, get_current_advertisement, add_new_advertisement, \
    add_new_notification, get_all_objects
from users.models import LanguageSkill


def show_advertisements_list(request):
    """список объявление """

    ads = get_all_objects(Advertisement)

    # Собираем языковые навыки для каждого объявления
    ads_with_languages = []
    for a in ads:
        user_language_skills = LanguageSkill.objects.filter(user=a.user)
        ads_with_languages.append({
            'ads': a,
            'language_skills': user_language_skills
        })

    data = {
        'ads_with_languages': ads_with_languages,
        'auth': request.user.is_authenticated,
        'user_id': request.user.id
    }

    return render(request, 'advertisements/ads_list.html', context=data)


@login_required
def show_selected_advertisement_view(request, slug_id):
    """страница отображения выборного объявления и списка других объявлений пользователя"""
    advertisement = get_current_advertisement(slug_id)
    avatar_url = advertisement.user.userprofile.avatar.url
    user_language_skills = LanguageSkill.objects.filter(user=request.user)

    if advertisement.user == request.user:
        return redirect('ads_list')

     
    data = {
        'auth': request.user.is_authenticated,
        'advertisement': advertisement,
        'avatar_url': avatar_url,
        'user_language_skills': user_language_skills,
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


def create_advertisement_handler(request):
    """добавление нового объявления в бд"""
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        return add_new_advertisement(request.user, form)


def delete_ads_handler(request, ads_id):
    ads = get_object_or_404(Advertisement, id=ads_id)

    if ads.user_id == request.user.id:
        ads.delete()
        return redirect('ads_list')


@login_required
def choose_advertisement_handler(request, slug_id):
    advertisement = Advertisement.objects.get(id=slug_id)

    add_new_notification(request.user, advertisement)

    room=f'{request.user}{advertisement.user.username}'
    return redirect('lesson', room)
