from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/', views.my_account, name='account'),
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('post/<str:postId>/', views.post, name='post'),
    path('saved/', views.saved, name='saved'),
    path('likes', views.likes, name='likes'),
    path('comment', views.addComment, name='comment'),
    path('upload', views.upload, name='upload'),
    path('delete', views.deletePost, name='delete'),
    path('save', views.save, name='save'),
    path('follow', views.follow, name='follow'),
    path('signup/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
]
