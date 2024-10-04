from django.urls import path
from advertisements import views


urlpatterns = [
    path('', views.advertisements_list, name='ads_list'),
    path('ads/<int:a>/', views.advertisements, name='ads1')

]
