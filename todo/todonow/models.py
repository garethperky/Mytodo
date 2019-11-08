from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone

VALUE_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),

)

class Todo(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, limit_choices_to={'groups__name': "Kids"}, on_delete=models.CASCADE)
    value = models.IntegerField(null=False, choices=VALUE_CHOICES)
    due_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('details', kwargs={'pk': self.pk})

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.first_name


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile, sender=User)
