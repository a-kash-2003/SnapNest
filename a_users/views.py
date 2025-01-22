from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth import logout
from django.contrib import messages
from .forms import *
from .models import *

# Create your views here.
def profile(request,username=None):
    if username:
        profile= get_object_or_404(User,username=username).profile
    else:
        try:
            profile= request.user.profile
        except:
            raise Http404
    return render(request,'a_users/profile.html',{'profile': profile})

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
    
