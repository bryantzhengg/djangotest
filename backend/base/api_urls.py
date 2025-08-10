from django.urls import path
from .views import get_all_posts, create_post, update_profile

urlpatterns = [
    path('feed/', get_all_posts),
    path('post/', create_post),
    path('update_profile/', update_profile),
] 