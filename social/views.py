import random
from .models import Profile, Post, PostLikes, SavedPosts, Follow, PostComments
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def home(request):
    ctx = {}
    if request.user.is_authenticated:
        ctx['firstName'] = request.user.first_name
        ctx['lastName'] = request.user.last_name
        
        profile_model = Profile.objects.get(id_user=request.user.id)
        ctx['profile'] = profile_model

        following = Follow.objects.filter(follower=request.user).values_list('user')
        posts = Post.objects.select_related('user').filter(user__in=following)
        ctx['posts'] = posts

        pk_ids = Profile.objects.exclude(user__in=following).values_list('id_user', flat=True)
        pks = random.sample([i for i in pk_ids if i != request.user.id], 4)
        ctx['suggestions'] = [Profile.objects.filter(id_user=pk).first() for pk in pks]
        
        ctx['status'] = ctx['suggestions']

    return render(request, 'body.html', ctx)


@login_required(login_url='login')
def my_account(request):
    ctx = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']
            bio = request.POST['bio']
            location = request.POST['location']
            profileImage = request.FILES.get('profileImage')
            User.objects.filter(username=request.user.username).update(first_name=firstName, last_name=lastName)
            if profileImage:
                Profile.objects.filter(id_user=request.user.id).update(bio=bio, location=location, profile_img=profileImage)
            else:
                Profile.objects.filter(id_user=request.user.id).update(bio=bio, location=location)
        user_model = User.objects.get(username=request.user.username)
        profile_model = Profile.objects.get(id_user=request.user.id)
        ctx['user'] = user_model
        ctx['profile'] = profile_model
        return render(request, 'my_account.html', ctx)
    return redirect('login')


def user_profile(request, username):
    try:
        profile_user = User.objects.get(username=username)
        profile_model = Profile.objects.get(id_user=profile_user.id)
        current_profile_model = Profile.objects.get(id_user=request.user.id)
        posts = Post.objects.filter(user=profile_user).order_by('-created_at')
        post_count = posts.count()
        is_followed = Follow.objects.filter(user=profile_user, follower=request.user)
        follower_count = Follow.objects.filter(user=profile_user).count()
        following_count = Follow.objects.filter(follower=profile_user).count()
    except:
        return redirect('home')
    ctx = { 'username': username,
            'owner': username == request.user.username,
            'bio': profile_model.bio,
            'profile_img': profile_model.profile_img,
            'profile': current_profile_model,
            'location': profile_model.location,
            'posts': posts,
            'post_count': post_count,
            'follower_count': follower_count,
            'following_count': following_count,
            'is_followed': is_followed
        }

    return render(request, 'user_profile.html', ctx)


@login_required(login_url='login')
def post(request, postId):
    post = Post.objects.get(id=postId)
    comments = PostComments.objects.filter(post=post).order_by('commented_on')
    ctx = {'post': post,
            'is_owner': post.user.username == request.user.username,
            'comments': comments
        }
    return render(request, 'post.html', ctx)


@login_required(login_url='login')
def saved(request):
    ctx = {}
    saved_posts = SavedPosts.objects.filter(user=request.user)
    ctx['saved_posts'] = saved_posts
    profile_model = Profile.objects.get(id_user=request.user.id)
    ctx['profile'] = profile_model
    return render(request, 'saved.html', ctx)
    

@login_required(login_url='login')
def upload(request):
    username = request.user.username
    if request.method == 'POST':
        caption = request.POST['caption']
        image = request.FILES.get('post_img')
        if caption is not None and caption != '' and image != '' and image is not None:
            user_model = User.objects.get(username=username)
            profile_model = Profile.objects.get(id_user=request.user.id)
            new_post = Post.objects.create(user=user_model, profile=profile_model, caption=caption, post_img=image)
            new_post.save()
        else:
            messages.info(request, 'Cannot be empty!')
    return redirect(f'profile/{username}')    

@login_required(login_url='login')
def deletePost(request):
    if request.method == 'POST':
        postId = request.POST['postId']
        post = Post.objects.get(id=postId)
        if post.user == request.user:
            post.delete()
    return redirect(f'profile/{request.user.username}')


@login_required(login_url='login')
def likes(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    post_likes = PostLikes.objects.filter(user=request.user, post=post).first()
    if post_likes is None:
        new_post_like = PostLikes.objects.create(user=request.user, post=post)
        new_post_like.save()
        post.increase_count()
    else:
        post_likes.delete()
        post.decrease_count()
    return redirect('/')

@login_required(login_url='login')
def addComment(request):
    if request.method == 'POST':
        postId = request.POST['postId']
        comment = request.POST['comment']
        post = Post.objects.get(id=postId)
        profile = Profile.objects.get(user=request.user)
        post_comment = PostComments.objects.create(profile=profile, post=post, comment=comment)
        post.increase_count_comments()
        post_comment.save()
        return redirect(f'post/{postId}')
    return redirect('/')


@login_required(login_url='login')
def save(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    post_save = SavedPosts.objects.filter(user=request.user, post=post).first()
    if post_save is None:
        new_post_like = SavedPosts.objects.create(user=request.user, post=post)
        new_post_like.save()
    else:
        post_save.delete()
    return redirect('/')


@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        username_to_follow = request.POST['username_to_follow']
        user_to_follow = User.objects.get(username=username_to_follow)
        is_follower = Follow.objects.filter(user=user_to_follow, follower=request.user).first()
        if is_follower is None:
            new_follower = Follow.objects.create(user=user_to_follow, follower=request.user)
            new_follower.save()
        else:
            is_follower.delete()
    return redirect(f'/profile/{username_to_follow}')


def signup_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        ctx = {
            "firstName":firstName,
            "lastName":lastName,
            "email":email,
            "username":username
            }
        if username == '' or password == '' or confirmPassword == '' or email == '' or firstName == '' or lastName == '':
            messages.info(request, 'Please enter all required fields')
            return render(request, 'signup.html', ctx)
        if password == confirmPassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists!')
                ctx['username'] = ''
                return render(request, 'signup.html', ctx)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists!')
                ctx['email'] = ''
                return render(request, 'signup.html', ctx)
            else:            
                user_model = User.objects.create_user(first_name=firstName, last_name=lastName, email=email, username=username, password=password)
                user_model.save()
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
        else:
            messages.info(request, 'Passwords do not match')
            return render(request, 'signup.html', ctx)
    return render(request, 'signup.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == '' or password == '':
            messages.info(request, 'Please enter all required fields')
            return render(request, 'login.html')
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password incorrect!')
                return render(request, 'login.html')
        else:
            messages.info(request, 'Username or password incorrect!')
    return render(request, 'login.html')
    
def logout_page(request):
    logout(request)
    return redirect('login')
