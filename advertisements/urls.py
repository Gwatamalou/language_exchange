from django.urls import path
from advertisements import views


urlpatterns = [
    path('<slug>', views.AdvertisementsList.as_view(), name='ads_list'),
    path('add-ads/', views.MakeAdvertisement.as_view(), name='add-ads'),

    path('<int:user_id>/', views.SelectedAdvertisement.as_view(), name='ads'),

]
