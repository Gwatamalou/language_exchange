from django.conf.urls.static import static
from django.urls import path

from language_exchange import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='main'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password-change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password-reset'),
    path('profile/<slug:user_id>/', views.show_user_profile_view, name='user-profile'),
    path('skills/', views.create_language_handler, name='create-skill'),
    path('update_skill/<int:skill_id>/', views.update_language_skill_handler, name='update-skill'),
    path('delete_skill/<int:skill_id>/', views.delete_language_skill_handler, name='delete-skill'),
    path('notification/', views.show_notification_view, name='notification-list'),
    path('notification/<int:notification_id>/', views.notification_response_handler, name='notification'),
    path('update-avatar/', views.update_avatar_handler, name='update-avatar'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)