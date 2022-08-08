from pyexpat import model
from django.db import models

# Create your models here.
class URL(models.Model):
    # original url
    link = models.URLField(max_length=200)
    # short url
    new_link = models.URLField(default='')
    
    