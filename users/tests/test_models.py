from django.templatetags.i18n import language
from django.test import TestCase
from django.contrib.auth.models import User


from users.models import UserProfile, LanguageSkill


class UserProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpass')
        UserProfile.objects.create(user=user, avatar='images/default.png')

    def test_one_to_one_field(self):
        user_profile = UserProfile.objects.get(id=1)
        field_user = user_profile._meta.get_field('user').verbose_name
        self.assertEqual(field_user, 'user')

    def test_avatar_field(self):
        user_profile = UserProfile.objects.get(id=1)
        field_avatar = user_profile._meta.get_field('avatar').verbose_name
        self.assertEqual(field_avatar, 'avatar')



class LanguageSkillModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpass')
        LanguageSkill.objects.create(user=user, language='English', level_skill='base')

    def test_one_to_one_field(self):
        language_skill = LanguageSkill.objects.get(id=1)
        field_user = language_skill._meta.get_field('user').verbose_name
        self.assertEqual(field_user, 'user')

    def test_language_field(self):
        language_skill = LanguageSkill.objects.get(id=1)
        field_language = language_skill._meta.get_field('language').verbose_name
        self.assertEqual(field_language, 'language')

    def test_level_skill_field(self):
        language_skill = LanguageSkill.objects.get(id=1)
        field_level_skill = language_skill._meta.get_field('level_skill').verbose_name
        self.assertEqual(field_level_skill, 'level skill')




