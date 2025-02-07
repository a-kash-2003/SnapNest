from django.contrib import admin
from .models import *

class InboxMessageAdmin(admin.ModelAdmin):
    readonly_fields=('body', 'converastion', 'sender')

admin.site.register(InboxMessage, InboxMessageAdmin)
admin.site.register(Converastion)