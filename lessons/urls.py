from django.urls import path

from lessons import views


urlpatterns = [
    path('<str:room>/', views.ConferenceView.as_view(), name='lesson'),
    ]
