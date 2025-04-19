from django.db import models
# Create your models here.


# shortcut




# models.py
from django.db import models

class Shortcut(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    icon_class = models.CharField(max_length=100, default='fa-solid fa-globe')

    def __str__(self):
        return self.name
