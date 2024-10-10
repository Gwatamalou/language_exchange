from django.urls import path
from setuptools.extern import names

from advertisements import views


urlpatterns = [
    path('', views.show_advertisements_list, name='ads_list'),
    path('add-ads/', views.show_make_advertisement_view, name='add-ads'),
    path('add-new-ads/', views.add_advertisement, name='add-new-ads'),
    path('<int:slug_id>/', views.show_selected_advertisement_view, name='ads'),
    path('choose/<int:slug_id>/', views.choose_advertisement_view, name='choose'),
    path('delete_das/<int:ads_id>/', views.delete_ads, name='delete_ads'),
]
