from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class MyUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, primary_key=True) #unique user, also as primary key
    bio = models.CharField(max_length=300)
    profile_image = models.ImageField(upload_to='profile_image/',blank=True, null=True)
    followers = models.ManyToManyField('self',symmetrical=False, related_name='following',blank=True)

    def __str__(self):
        return self.username

# needs to be able to passed through api, so this information needs to be in .json. create serializer...

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    time_spent = models.CharField(max_length=20, blank=True, null=True)
    topic = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"

