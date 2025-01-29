from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from .models import *
from .forms import *
from bs4 import BeautifulSoup
import requests
from django.contrib import messages


def home(request, tag=None):
    if tag:
        post=Post.objects.filter(tags__slug=tag)
        tag=get_object_or_404(Tag, slug=tag)
    else:
        post=Post.objects.all()
    categories=Tag.objects.all()
    context={
        'posts': post,
        'categories': categories,
        'tag': tag
    }
    return render(request,'a_posts/home.html',context)


@login_required
def post_create(request):
    form=PostCreateForm()
    if request.POST:
        form=PostCreateForm(request.POST)
        if form.is_valid:
            post=form.save(commit=False)

            website=requests.get(form.data['url'])
            sourcecode=BeautifulSoup(website.text,'html.parser')

            find_image=sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            image=find_image[0]['content']
            post.image=image

            find_title=sourcecode.select('h1.photo-title')
            title=find_title[0].text.strip()
            post.title=title

            find_artist=sourcecode.select('a.owner-name')
            artist=find_artist[0].text.strip()
            post.artist=artist

            post.author=request.user

            post.save()
            form.save_m2m()
            return redirect('home')
    context={'form':form}
    return render(request,'a_posts/post_create.html',context)


@login_required
def post_delete(request, pk):
    post=get_object_or_404(Post,id=pk,author=request.user)
    if request.POST:
        post.delete()
        messages.success(request,'Post Deleted')
        return redirect('home')
    context={'post':post}
    return render(request,'a_posts/post_delete.html',context)


@login_required
def post_edit(request, pk):
    post=get_object_or_404(Post,id=pk,author=request.user)
    form=PostEditForm(instance=post)
    if request.POST:
        form=PostEditForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'Post Updated')
            return redirect('home')
    context={
        'post':post,
        'form':form
        }
    return render(request,'a_posts/post_edit.html',context)


def post_page(request, pk):
    post=get_object_or_404(Post,id=pk)
    commentform=CommentForm()
    replyform=ReplyForm()
    if request.htmx:
        if 'top' in request.GET:
            # comments=post.comments.filter(likes__isnull=False).distinct()
            comments=post.comments.annotate(like_count=Count('likes')).filter(like_count__gt=0).order_by('-like_count')
        else:
            comments=post.comments.all()
        return render(request,'snippets/loop_postpage_comment.html',{'comments':comments,'replyform':replyform})
    context={
        'post':post,
        'commentform':commentform,
        'replyform':replyform
    }
    return render(request,'a_posts/post_page.html',context)


@login_required
def comment_add(request, pk):
    post=get_object_or_404(Post,id=pk)
    replyform=ReplyForm()
    if request.POST:
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author=request.user
            comment.post=post
            comment.save()
    context={
        'post':post,
        'comment':comment,
        'replyform':replyform
    }
    return render(request,'snippets/add_comment.html', context)


@login_required
def reply_add(request, pk):
    comment=get_object_or_404(Comment,id=pk)
    replyform=ReplyForm()
    if request.POST:
        form=ReplyForm(request.POST)
        if form.is_valid():
            reply=form.save(commit=False)
            reply.author=request.user
            reply.comment=comment
            reply.save()
    context={
        'reply':reply,
        'comment':comment,
        'replyform':replyform
    }
    return render(request,'snippets/add_reply.html', context)


@login_required
def comment_delete(request, pk):
    comment=get_object_or_404(Comment, id=pk, author=request.user)
    if request.POST:
        comment.delete()
        messages.success(request,'Comment Deleted')
        return redirect('post_page', comment.post.id)
    return render(request,'a_posts/comment_delete.html', {'comment':comment})


@login_required
def reply_delete(request, pk):
    reply=get_object_or_404(Reply, id=pk, author=request.user)
    if request.POST:
        reply.delete()
        messages.success(request,'Reply Deleted')
        return redirect('post_page', reply.comment.post.id)
    return render(request,'a_posts/reply_delete.html', {'reply':reply})


def like_toggle(model):
    def inner_func(func):
        def wrapper(request,pk):
            obj= get_object_or_404(model, id=pk)
            user_exists= obj.likes.filter(username=request.user.username).exists()
            if obj.author != request.user:
                if user_exists:
                    obj.likes.remove(request.user)
                else:
                    obj.likes.add(request.user)
            return func(request, obj)
        return wrapper
    return inner_func

@login_required
@like_toggle(Post)
def like_post(request, obj):
    return render(request,'snippets/like_post.html',{'post':obj})

@login_required
@like_toggle(Comment)
def like_comment(request, obj):
    return render(request,'snippets/like_comment.html',{'comment':obj})

@login_required
@like_toggle(Reply)
def like_reply(request, obj):
    return render(request,'snippets/like_reply.html',{'reply':obj})