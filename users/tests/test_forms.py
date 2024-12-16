from django.test import TestCase
from users.forms import LanguageSkillForm, AvatarForm

class LanguageSkillFormTest(TestCase):

    def test_language_skill_form(self):
        form = LanguageSkillForm(data={'language': 'Английский', 'level_skill': 'начальный'})
        self.assertTrue(form.is_valid())


class AvatarFormTest(TestCase):

    def test_avatar_form(self):
        form = AvatarForm(data={'avatar': 'images/default.png'})
        self.assertTrue(form.is_valid())



