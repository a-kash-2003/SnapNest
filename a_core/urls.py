"""
URL configuration for a_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from a_posts.views import *
from a_users.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', home, name='home'),
    path('category/<tag>', home, name='category'),
    path('post/create/', post_create, name='create'),
    path('post/delete/<pk>/', post_delete, name='delete'),
    path('post/edit/<pk>/', post_edit, name='edit'),
    path('post/post_page/<pk>/', post_page, name='post_page'),
    path('profile/', profile, name='profile'),
    path('<username>', profile, name='profile_visit'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/delete/', profile_delete, name='profile_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)