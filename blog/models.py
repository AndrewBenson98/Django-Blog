from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=CASCADE)
    date_published = models.DateField(blank=True, null=True)
    
    
    def __str__(self):
        return self.title
    
    #Works with class create view to redirect after post is created
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})
    
    