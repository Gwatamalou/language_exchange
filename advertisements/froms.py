from .models import Advertisement
from django.forms import ModelForm

class AdvertisementForm(ModelForm):
    class Meta:
        model = Advertisement
        fields = ['language_to_learn', 'language_level_to_learn',]
