from django.urls import path

from lessons import views


urlpatterns = [
    path('<str:room>/', views.show_conference_view, name='lesson'),
    ]
