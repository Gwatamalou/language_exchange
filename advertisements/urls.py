from django.urls import path
from advertisements import views


urlpatterns = [
    path('', views.show_advertisements_list, name='ads_list'),
    path('<slug:slug_id>/', views.show_selected_advertisement_view)

]
