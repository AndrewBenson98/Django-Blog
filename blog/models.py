from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(verbose_name="Comment")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=CASCADE)
    date_published = models.DateField(blank=True, null=True)
    
    
    def __str__(self):
        return self.title
    
    #Works with class create view to redirect after post is created
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    
    def approve(self):
        self.approved_comment = True
        self.save()
        
    def __str__(self):
        return self.content
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    
