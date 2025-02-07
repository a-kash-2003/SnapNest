from django.urls import path
from .views import *

urlpatterns = [
    path('', inbox_view, name='inbox'),
    path('c/<conversation_id>/', inbox_view, name='inbox'),
    path('search_users/', search_users, name='inbox_searchusers'),
    path('new_message/<recipient_id>', new_message, name='inbox_newmessage'),
    path('new_reply/<conversation_id>', new_reply, name='inbox_newreply'),
    path('notify/<conversation_id>', notify_newmessage, name='notify_newmessage'),
    path('notify_inbox', notify_inbox, name='notify_inbox'),


]