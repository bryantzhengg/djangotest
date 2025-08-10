from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64
import re

from .models import MyUser, Post
from .serializer import MyUserProfileSerializer, PostSerializer
from django.contrib.auth.decorators import login_required


@api_view(['GET'])
def get_user_profile_data(request, pk):
    try:
        user = MyUser.objects.get(username=pk)
    except MyUser.DoesNotExist:
        return Response({'error': 'This user does not exist.'})
    
    serializer = MyUserProfileSerializer(user, many=False)
    return Response(serializer.data)


def profile_page(request, username):
    if not request.user.is_authenticated:
        return redirect('not_logged_in')
    return render(request, 'profile.html', {'username': username})


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', username=user.username)
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


@login_required
def my_profile_redirect(request):
    return redirect('profile', username=request.user.username)


# ======== POSTS API ========

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.bio = data.get('bio', user.bio)

    # Handle profile image upload/removal
    remove_image = data.get('remove_image', 'false') == 'true'
    profile_image_data = data.get('profile_image', None)
    if remove_image:
        if user.profile_image:
            user.profile_image.delete(save=False)
        user.profile_image = None
    elif profile_image_data:
        match = re.match(r'data:image/(?P<ext>\w+);base64,(?P<data>.+)', profile_image_data)
        if match:
            ext = match.group('ext')
            img_data = base64.b64decode(match.group('data'))
            filename = f"profile_{user.username}.{ext}"
            user.profile_image.save(filename, ContentFile(img_data), save=False)
    user.save()
    # Always return the default image if none is set
    default_img = '/static/img/default_profile.png'
    profile_img_url = user.profile_image.url if user.profile_image else default_img
    return Response({
        'success': True,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'bio': user.bio,
        'profile_image': profile_img_url
    })

def feed_page(request):
    if not request.user.is_authenticated:
        return redirect('not_logged_in')
    return render(request, 'feed.html')


def not_logged_in(request):
    return render(request, 'not_logged_in.html')