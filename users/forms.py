from .models import LanguageSkill
from django.forms import ModelForm
from .models import UserProfile

class LanguageSkillForm(ModelForm):
    class Meta:
        model = LanguageSkill
        fields = ['language', 'level_skill']


class AvatarForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']