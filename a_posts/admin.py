from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Like_post)
admin.site.register(Like_comment)
admin.site.register(Like_reply)





