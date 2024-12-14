from django.db import models
from django.urls import reverse

class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(help_text="Main content of the newsletter")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
