from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=500)
    artist=models.CharField(max_length=500,null=True)
    url=models.URLField(max_length=500,null=True)
    author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='posts')
    image=models.URLField(max_length=500)
    body=models.TextField()
    likes=models.ManyToManyField(User,related_name='liked_post',through='Like_post')
    tags=models.ManyToManyField('Tag')
    created=models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100, default=uuid.uuid4, primary_key=True, editable=False,unique=True)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering=['-created']


class Like_post(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.post.title}'


class Tag(models.Model):
    name=models.CharField(max_length=20)
    image=models.FileField(upload_to='icons/',null=True,blank=True)
    slug=models.SlugField(max_length=20,unique=True)
    order=models.IntegerField(null=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering=['order']

  
class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    body=models.CharField(max_length=150)
    likes=models.ManyToManyField(User,related_name='liked_comment',through='Like_comment')
    created=models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100, default=uuid.uuid4, primary_key=True, editable=False,unique=True)

    def __str__(self):
        try:
            return str(f'{self.author} : {self.body}')
        except:
            return str(f'No author : {self.body[:30]}')
        
    class Meta:
        ordering=['-created']


class Like_comment(models.Model):
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.comment.body[:30]}'


class Reply(models.Model):
    comment=models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='replies')
    body=models.CharField(max_length=150)
    likes=models.ManyToManyField(User,related_name='liked_reply',through='Like_reply')
    created=models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100, default=uuid.uuid4, primary_key=True, editable=False,unique=True)

    def __str__(self):
        try:
            return str(f'{self.author} : {self.body}')
        except:
            return str(f'No author : {self.body[:30]}')
        
    class Meta:
        ordering=['-created']


class Like_reply(models.Model):
    reply=models.ForeignKey(Reply,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.reply.body[:30]}'