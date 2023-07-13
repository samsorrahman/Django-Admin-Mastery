from django.db import models

# Create your models here.

class Blog(models.Model):
    title= models.CharField(max_length=255)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=True)
    slug = models.SlugField(max_length=250, blank=True)
    
    
    def __str__(self):
        return self.title