from django.urls import path
from lessons import views


urlpatterns = [
    path('', views.lesson, name='lesson'),
    path('conference/', views.conference)
]
