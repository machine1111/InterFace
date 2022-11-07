from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images', default='default.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_img = models.ImageField(upload_to='posts_images', blank=False)
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
    def increase_count(self):
        self.likes += 1
        self.save()

    def decrease_count(self):
        self.likes -= 1
        self.save()

    def increase_count_comments(self):
        self.comments += 1
        self.save()

    def decrease_count_comments(self):
        self.comments -= 1
        self.save()

class PostLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class PostComments(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=False, blank=False)
    commented_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile.user.username

class SavedPosts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to_follow')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

    def __str__(self):
        return self.user.username