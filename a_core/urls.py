
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
    path('profile/onboarding/', profile_edit, name='profile_onboarding'),
    path('comment/<pk>/', comment_add, name='comment'),
    path('comment/delete/<pk>/', comment_delete, name='comment_delete'),
    path('reply/<pk>/', reply_add, name='reply'),
    path('reply/delete/<pk>/', reply_delete, name='reply_delete'),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)