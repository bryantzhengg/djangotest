from rest_framework import serializers
from .models import MyUser, Post

class MyUserProfileSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'bio', 'profile_image', 'follower_count', 'following_count']

    def get_follower_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()

    def get_profile_image(self, obj):
        # Solid green circle SVG as URL-encoded data URI
        default_img = 'data:image/svg+xml;utf8,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20width%3D%27100%27%20height%3D%27100%27%3E%3Ccircle%20cx%3D%2750%27%20cy%3D%2750%27%20r%3D%2750%27%20fill%3D%27%236be38f%27/%3E%3C/svg%3E'
        return obj.profile_image.url if obj.profile_image else default_img

class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'username', 'content', 'created_at', 'time_spent', 'topic']

    def get_username(self, obj):
        return obj.user.username if obj.user else "unknown"
