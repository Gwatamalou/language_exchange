from django.urls import path
from advertisements import views


urlpatterns = [
    path('', views.advertisements_list, name='ads_list'),
    path('<slug:slug_id>/', views.advertisements)

]
