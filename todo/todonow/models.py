from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Todo(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(null=False)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.first_name

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile, sender=User)
