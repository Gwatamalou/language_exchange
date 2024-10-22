from django.shortcuts import redirect
from advertisements.models import Advertisement, Notification
from users.services import get_object_or_error, get_object_if_any


def get_current_advertisement(slug_id):
    return get_object_or_error(Advertisement, id=slug_id)

def get_advertisement_user(user_id):
    return get_object_if_any(Advertisement, user_id=user_id)

def get_all_objects(model):
    return model.objects.all()

def add_new_advertisement(user, form):
    if form.is_valid():
        advertisement = form.save(commit=False)
        advertisement.user = user
        advertisement.save()
        return redirect('ads_list')
    return None

def add_new_notification(user, ads):
    if not Notification.objects.filter(responder=user, user=ads.user, advertisement=ads).exists():
        Notification.objects.create(
            responder=user,
            user=ads.user,
            advertisement=ads,
            room=f'{user}{ads.user.username}',
        )

