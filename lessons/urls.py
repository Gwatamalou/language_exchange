from django.urls import path

from lessons import views


urlpatterns = [
    path('', views.show_user_lesson_view, name='lesson'),
    path('conference/', views.show_conference_view, name='conference'),
]
