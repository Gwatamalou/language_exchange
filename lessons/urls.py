from django.urls import path

from lessons import views


urlpatterns = [
    path('', views.show_conference_view, name='lesson'),
    ]
