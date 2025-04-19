from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # city = models.ForeignKey('City', related_name='user_city', on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='profile/', blank=True, null=True)

    def delete(self, *args, **kwargs):
        # Delete the associated image file
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)
    def __str__(self):
        return str(self.user)
    


@receiver(post_save, sender=User)      
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



       