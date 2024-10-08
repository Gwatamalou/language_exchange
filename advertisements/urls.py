from django.urls import path
from setuptools.extern import names

from advertisements import views


urlpatterns = [
    path('', views.show_advertisements_list, name='ads_list'),
    path('add-ads/', views.show_make_advertisement_view, name='add-ads'),
    path('add-new-ads/', views.add_advertisement, name='add-new-ads'),
    path('<slug:slug_id>/', views.show_selected_advertisement_view, name='ads'),


]
