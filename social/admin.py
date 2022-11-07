from django.contrib import admin
from .models import Profile, Post, PostLikes, SavedPosts, Follow, PostComments

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostLikes)
admin.site.register(SavedPosts)
admin.site.register(Follow)
admin.site.register(PostComments)