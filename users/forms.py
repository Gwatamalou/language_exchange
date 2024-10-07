from .models import LanguageSkill
from django.forms import ModelForm

class LanguageSkillForm(ModelForm):
    class Meta:
        model = LanguageSkill
        fields = ['language', 'level_skill']