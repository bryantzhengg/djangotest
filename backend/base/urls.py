from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from .views import get_user_profile_data, profile_page, signup_view, my_profile_redirect, feed_page, not_logged_in

urlpatterns = [
    path('user_data/<str:pk>/', get_user_profile_data),
    path('users/<str:username>/', profile_page, name='profile'),

    #auth routes
    path('signup/', signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('me/', my_profile_redirect, name='my-profile'),

    path('feed/', feed_page, name='feed'),
    path('not-logged-in/', not_logged_in, name='not_logged_in'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
