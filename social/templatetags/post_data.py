from django import template
from social.models import PostLikes, SavedPosts

register = template.Library()

@register.simple_tag
def is_post_liked(user, post):
    post_likes = PostLikes.objects.filter(user=user, post=post)
    return len(post_likes)

@register.simple_tag
def is_post_saved(user, post):
    post_saved = SavedPosts.objects.filter(user=user, post=post)
    return len(post_saved)