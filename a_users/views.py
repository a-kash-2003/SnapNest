from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth import logout
from django.db.models import Count
from django.contrib import messages
from .forms import *
from a_posts.forms import ReplyForm
from .models import *
from a_inbox.forms import InboxNewMessageForm

# Create your views here.
def profile(request,username=None):
    if username:
        profile= get_object_or_404(User,username=username).profile
    else:
        try:
            profile= request.user.profile
        except:
            raise Http404
    posts=profile.user.posts.all()
    if request.htmx:
        if 'top-posts' in request.GET:
            posts=profile.user.posts.annotate(like_count=Count('likes')).filter(like_count__gt=0).order_by('-like_count')
        elif 'top-comments' in request.GET:
            comments=profile.user.comments.annotate(like_count=Count('likes')).filter(like_count__gt=0).order_by('-like_count')
            replyform=ReplyForm
            return render(request,'snippets/loop_profile_comments.html', {'comments': comments, 'replyform': replyform})
        elif 'liked-posts' in request.GET:
            posts=profile.user.liked_post.order_by('-like_post__created')
        return render(request,'snippets/loop_profile_posts.html', {'posts': posts})
    
    new_message_form=InboxNewMessageForm()

    context={
        'profile': profile,
        'posts': posts,
        'new_message_form':new_message_form,
    }
    return render(request,'a_users/profile.html', context)


@login_required
def profile_edit(request):
    form=ProfileEditForm(instance=request.user.profile)
    if request.POST:
        form=ProfileEditForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    if request.path == reverse('profile_onboarding'):
        template = 'a_users/profile_onboarding.html'
    else:
        template = 'a_users/profile_edit.html'
    return render(request, template, {'form' : form})


@login_required
def profile_delete(request):
    user= request.user
    if request.POST:
        logout(request)
        user.delete()
        messages.success(request,'Account deleted, what a pity!')
        return redirect('home')
    return render(request,'a_users/profile_delete.html')
    
