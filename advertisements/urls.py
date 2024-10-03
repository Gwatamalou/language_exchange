from django.urls import path
from advertisements import views


urlpatterns = [
    path('', views.advertisements, name='ads'),
]
