from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='user'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('profile/<int:user_id>/', views.show_user_profile_view, name='user_profile'),
    path('add-skill/', views.add_new_language, name='add_skill'),
    path('update-skill/<int:skill_id>/', views.update_language_skill_view, name='update_skill'),
    path('delete-skill/<int:skill_id>/', views.delete_language_skill_view, name='delete_skill'),

]