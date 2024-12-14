from django.conf.urls.static import static
from django.urls import path

from language_exchange import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='main'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password-change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password-reset'),
    path('profile/<slug:user_id>/', views.UserProfileView.as_view(), name='user-profile'),
    # path('update_skill/<int:skill_id>/', views.UpdateLanguageSkillView.as_view(), name='update-skill'),
    path('notification/', views.NotificationView.as_view(), name='notification-list'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)