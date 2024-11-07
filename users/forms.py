from .models import LanguageSkill
from django.forms import ModelForm
from .models import UserProfile

class LanguageSkillForm(ModelForm):
    class Meta:
        model = LanguageSkill
        fields = ['language', 'level_skill']

    def __init__(self, *args, language_readonly=False, **kwargs):
        super(LanguageSkillForm, self).__init__(*args, **kwargs)
        if language_readonly:
            self.fields['language'].disabled = True

class AvatarForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

