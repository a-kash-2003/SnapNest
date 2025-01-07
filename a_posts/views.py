from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from bs4 import BeautifulSoup
import requests
from django.contrib import messages

# Create your views here.
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
    context={
        'post':post
    }
    return render(request,'a_posts/post_page.html',context)