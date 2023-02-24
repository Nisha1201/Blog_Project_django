from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import  ProfileForm,PostForm,UserForm
from .models import Profile, Post
from django.contrib.auth.models import User
import pdb
from django.urls import reverse
def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'signup.html', {'user_form': user_form,'profile_form': profile_form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:  
                login(request, user)
                return redirect('profile')

        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'login.html')

@login_required
def update(request):
    profile = get_object_or_404(Profile, user=request.user)
    user_name=request.user
    # user=get_object_or_404(User)
    # print(user,"slknldslknskllkdn")
    if request.method == 'POST':
        print(request.POST,"HHHHHHHHHHHHHHHHHHHHHHHH")
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        # user_form = UserForm(instance=user)
        form = ProfileForm(instance=profile)
        
    context = {'form': form,'name':user_name}
    return render(request, 'update.html', context)

@login_required
# @user_passes_test(user_login)
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    profile_details=Profile.objects.filter(user=request.user)
    user = User.objects.filter(username=request.user)
    print(profile)
    context = {'details':profile_details,'user':user}
    return render(request,'profile.html',context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.save()
            messages.success(request, 'Post created successfully')
            return redirect('home')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'create_post.html', context)


@login_required
def like_post(request, id):
    print(id,"idddddddddddddddd")
    post = get_object_or_404(Post, id=id)
    print('pooooooooooossstttttttt',post)
    if request.method == 'POST':
        print(request.method,"----------------------")
        if request.user in post.likes.all():
            # user has already liked the post, remove their like
            post.likes.remove(request.user)
        else:
            # user has not liked the post yet, add their like and remove dislike
            post.likes.add(request.user)
            # post.dislikes.remove(request.user)
    print("loginnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
    return redirect('home')

@login_required
def dislike_post(request, id):
    print(id,"aaaaaaaaaaaaaaaaaaaaaaaa")
    post = get_object_or_404(Post, id=id)
    print('bbbbbbbbbbbbbbbbbbbbbb',post)
    if request.method == 'POST':
        print(request.method,"cccccccccccccccccccccccccccccccccc")
        if request.user in post.dislikes.all():
            # user has already disliked the post, remove their dislike
            post.dislikes.remove(request.user)
        else:
            # user has not disliked the post yet, add their dislike and remove like
            post.dislikes.add(request.user)
            post.likes.remove(request.user)
    return redirect('home')

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    # form = PostForm()
    # print(form,'pppppppppppppppppppppppppppppppp')
    if request.user.id is not None:
        user_id=request.user.id
        print(user_id)
        liked_list=[]
        like_post=Post.objects.filter(likes=user_id)
        for i in like_post:
            liked_list.append(i.title)
        print(like_post)
        print("lnkjanjknjknkjsbahjbjkbsakj-----------------")
        context = {'posts': posts,'user_id':user_id,'liked_list':liked_list}
    else:
        context = {'posts': posts}
    print("bhjasbhjbkjsha",posts)
    return render(request, 'home.html', context)

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('home')

    context = {'post': post}
    return render(request, 'delete_post.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')


