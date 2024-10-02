from django.contrib import admin
from .models import UserProfile, LengthSkill, Advertisement, Lesson


admin.site.register(UserProfile)
admin.site.register(LengthSkill)
admin.site.register(Advertisement)
admin.site.register(Lesson)