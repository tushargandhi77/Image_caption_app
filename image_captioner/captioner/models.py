from django.db import models

# Create your models here.
class Caption(models.Model):
    image = models.ImageField(upload_to='images/')
    platform = models.CharField(max_length=50)
    num_captions = models.IntegerField()
    generated_captions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)