from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.show_user_profile_view, name='user'),
]

